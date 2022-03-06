package com.idse.pipelinescript.service.impl;

import com.idse.pipelinescript.pojo.pipeline.Component;
import com.idse.pipelinescript.pojo.pipeline.ComponentInputParam;
import com.idse.pipelinescript.pojo.pipeline.Param;
import com.idse.pipelinescript.pojo.pipeline.Pipeline;
import com.idse.pipelinescript.service.intf.GenerateScriptService;
import com.idse.pipelinescript.utils.FileUtils;
import com.idse.pipelinescript.utils.generate.code.intf.GenerateCode;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

import javax.annotation.Resource;
import java.io.*;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

import static java.util.regex.Pattern.compile;

/**
 * @Author dailinfeng
 * @Description TODO
 * @Date 2022/2/26 9:40 AM
 * @Version 1.0
 */
@Service
@Slf4j
public class GenerateScriptImpl implements GenerateScriptService {

    @Resource
    GenerateCode generateCode;

    /**
     * pipeline生成yaml的文件
     *
     * @param pipeline
     * @return
     * @throws IOException
     */
    @Override
    public boolean generateYaml(Pipeline pipeline) throws IOException {
        StringBuilder res = new StringBuilder();

        /**
         * 添加import
         */
        res.append("import kfp\r\n");
        res.append("from kfp.v2 import dsl\r\n");
        res.append("from kfp.v2.dsl import component\r\n");
        res.append("from kfp.v2.dsl import component, Input, Output, OutputPath, Dataset, Model,InputPath\r\n");
        res.append("import kfp.components as comp\r\n");


        /**
         * 添加加载组件的代码
         */
        //获取组件列表
        List<Component> components = pipeline.getComponents();
        Set<String> urlSet = new HashSet<>();
        //根据组件列表引入组件
        for (Component component : components) {
            String componentUrl = component.getUrl();
            String funcName = component.getFuncName();
            if (urlSet.contains(componentUrl)) {
                continue;
            }
            res.append(funcName).append("=").append("comp.load_component_from_url('").append(componentUrl).append("')\r\n");
            urlSet.add(componentUrl);
        }
        /**
         * 添加注解
         */
        //@dsl.pipeline(name='addition-pipelineaaa',description='An example pipeline that performs addition calculations.')
        //添加注解
        res.append("@dsl.pipeline(name='").append(pipeline.getPipelineName()).append("',description='").append(pipeline.getDescription()).append("')\r\n");
        res.append("def  ").append(pipeline.getPipelineFuncName()).append("(");
        for (Param param : pipeline.getPipelineParams()) {
            res.append(param.getName()).append(":").append(param.getType()).append("=").append(param.getDefaultValue()).append(",");
        }
        res.append("):\r\n");

        //将节点列表转换成map并添加返回值
        Map<String, Component> componentMap = generateCode.getComponentMap(pipeline.getComponents());
        /**
         * 添加调用组件代码
         */
        // first_add_task = add(a, b)
        for (Component component : pipeline.getComponents()) {
            //调用方法的代码
            res.append("    ")
                    .append(component.getResValueName())
                    .append("=").append(component.getFuncName()).append("(");
            //添加参数
            for (ComponentInputParam componentInputParam : component.getComponentInputParams()) {
                //如果来源是pipeline方法参数上的
                if (componentInputParam.getPipelineParam()) {
                    res.append(componentInputParam.getName()).append("=").append(componentInputParam.getPipelineParamName()).append(",");
                } else {
                    //获取上一个组件
                    Component preComponent = componentMap.get(componentInputParam.getOriginCompoId());
                    //添加一个参数
                    res.append(componentInputParam.getName())
                            .append("=")
                            .append(preComponent.getResValueName()).append(".output,");
                }

            }
            res.append(")\r\n");
        }

        /**
         * 写入文件
         */
        String fileName = generateCode.getComponentName() + ".py";
        BufferedWriter writer = new BufferedWriter(new FileWriter(fileName));
        writer.write(res.toString());
        writer.close();
        log.info(fileName);
        return true;
    }

    /**
     * 读取python文件对代码进行改造
     * * @param filePath
     *
     * @return
     */
    @Override
    public String generateComponent(String filePath) throws IOException, InterruptedException {
        //以行为单位读取文件
        List<String> codeLines = FileUtils.readSourceCode(filePath);
        //方法返回元数据名称栈，主要用于return代码替换的时候找到当前return对应的是哪一个元数据返回
        Stack<String> funcReturnMetaStack = new Stack<>();
        /**
         * 删除代码中的一切中文包括中文标点符号
         *  有bug：
         *      1.包含就删掉整行，如果中文写在代码内代码将被删除
         */
        List<String> noChineseCodes = codeLines.stream().filter(e -> !generateCode.containChinese(e)).collect(Collectors.toList());
        /**
         * 获取导包语句
         */
        List<String> importCodes = noChineseCodes.parallelStream().filter(e -> e.startsWith("import ") || e.startsWith("from ")).collect(Collectors.toList());
        //添加joblib的包
        importCodes.add("import joblib");
        /**
         *处理方法定义语句上的参数更改
         */
        //检测方法语句,结束后返回的是转换好的方法定义
        List<String> transferMethods = new ArrayList<>();
        //参数加载命令map
        HashMap<String, List<String>> paramsLoadMap = new HashMap<>();

        for (String code : noChineseCodes) {
            //表示这是一个方法定义的代码
            if (code.startsWith("def ") && code.strip().endsWith(":")) {
                /**
                 * 假设匹配的是def fun2_min(params=10, x:int=10, y):
                 * 第一个正则是匹配的方法名 def fun2_min
                 * 第二个正则是匹配的参数  (params=10, x:int=10, y)，这个正则没有考虑参数的默认值是调用方法的情况 比如 params=add()
                 *
                 */
                //匹配到定义方法和方法名
                Pattern methodName = compile("^def[ ]{1,}[0-9a-zA-Z_ ]*");
                //匹配到方法的参数
                Pattern paramsName = compile("\\([0-9a-zA-Z_ :=,!]*\\)");
                Matcher methodM = methodName.matcher(code.strip());
                Matcher paramsM = paramsName.matcher(code.strip());
                log.info("当前处理的方法为" + code);
                //如果这个能够匹配到表示他是一个方法
                if (methodM.find()) {
                    //假设code为 def fun2_min(params=10, x:int=10, y):
                    //这个匹配到的是 def fun2_min
                    String funcName = methodM.group();
                    //开始拼接
                    StringBuilder replaceCode = new StringBuilder(funcName);
                    replaceCode.append("(");
                    //如果方法有参数就对参数进行处理
                    if (paramsM.find()) {
                        log.info("当前方法的参数列表为" + paramsM.group());
                        //这个匹配到的是 (params=10, x:int=10, y)
                        StringBuilder paramsStr = new StringBuilder(paramsM.group());
                        //删除最前面的(
                        paramsStr.replace(0, 1, "");
                        //删除最后面的(
                        paramsStr.replace(paramsStr.length() - 1, paramsStr.length(), "");
                        List<String> variable = List.of(paramsStr.toString().split(","));
                        //匹配参数名字，因为名字里还有默认值那些
                        Pattern variableName = compile("^[0-9a-zA-Z_ ]*");
                        //传给其他部分的单个参数名称 list
                        List<String> singleParamNames = new LinkedList<>();
                        for (String param : variable) {
                            Matcher paramM = variableName.matcher(param.strip());
                            paramM.find();
                            String paramStr = paramM.group();
                            log.info("参数名称为:" + paramStr);
                            singleParamNames.add(paramStr);
                            replaceCode.append(paramStr);
                            //添加输入  输入的文件名为xxx_path
                            replaceCode.append("_path:Input[Dataset],");
                        }
                        //添加参数名到参数map，后面需要加载参数
                        paramsLoadMap.put(funcName.replaceAll("def", "").strip(), new ArrayList<>(singleParamNames));
                    }

                    //添加返回值的参数，返回值的变量名规则是:方法名_return:
                    String outputPath = funcName.replaceAll("def", "").strip() + "_return";
                    //添加当前方法返回元数据到栈中
                    funcReturnMetaStack.push(outputPath);
                    replaceCode.append(outputPath);
                    replaceCode.append(": Output[Dataset]");
                    //添加): 方法定义语句最后两个字符  出现->int 这种的情况直接屏蔽 全部使用joblib的这种通用方式
                    replaceCode.append("):");
                    transferMethods.add(replaceCode.toString());
                }
            } else {
                //如果不是方法定义代码
                transferMethods.add(code);
            }

        }
        /**
         * 在方法定义代码的下一行添加import 语句代码
         * 在方法定义的上一行添加组件的定义装饰器
         * 在import的下一行添加参数的加载代码  从joblib中加载参数值
         * 匹配到return语句，对return进行改造
         */
        //当前的代码，用于在代码列表上插入其他代码
        List<String> currentCodes = new LinkedList<>();
        /**
         * 在代码上面加上导pipeline component相关的包
         * import kfp
         * from kfp.v2 import dsl
         * from kfp.v2.dsl import component
         * from kfp.v2.dsl import component, Input, Output, OutputPath, Dataset, Model,InputPath
         * import kfp.components as comp
         */

        currentCodes.add("import kfp");
        currentCodes.add("from kfp.v2 import dsl");
        currentCodes.add("from kfp.v2.dsl import component, Input, Output, OutputPath, Dataset, Model,InputPath");
        currentCodes.add("import kfp.components as comp");

        //在转换好的方法体最前面加上导包语句
        for (String code : transferMethods) {
            //使用一行代码的开头为def 结尾为:判断这行代码是方法定义
            //如果是方法定义代码就在这行代码的下一行加上导包的语句
            if (code.strip().startsWith("def ") && code.strip().endsWith(":")) {
                /**
                 * 在方法定义代码上添加组件定义代码
                 */
                //匹配到定义方法和方法名
                Pattern methodNamePattern = compile("^def[ ]{1,}[0-9a-zA-Z_ ]*");
                Matcher methodNameMatchar = methodNamePattern.matcher(code.strip());
                methodNameMatchar.find();
                //方法名
                String method = methodNameMatchar.group().replaceAll("def ", "").strip();
                StringBuilder componentCode = new StringBuilder();
                //@component(output_component_file='get_model1.yaml',packages_to_install=['lmfit','joblib','pandas',])
                //添加前面部分
                componentCode.append("@component(output_component_file='");
                //添加方法名 导出的组件名为 方法名_component.yaml
                componentCode.append(method);
                componentCode.append("_component.yaml',packages_to_install=[");
                //寻找依赖的包
                List<String> dependences = generateCode.getDependences(importCodes);
                for (String dependence : dependences) {
                    componentCode.append(dependence);
                    componentCode.append(",");
                }
                //添加依赖包的结尾
                componentCode.append("])");
                //添加组件定义代码
                currentCodes.add(componentCode.toString());
                /**
                 * 在方法定义语句下添加import语句
                 */
                // 方法定义语句
                currentCodes.add(code);
                //import语句添加
                int importSize = importCodes.size();
                for (int i = 0; i < importSize; i++) {
                    //添加import语句在方法定义语句下面
                    currentCodes.add("    " + importCodes.get(i));
                }
                /**
                 * import 之后是加载参数的代码
                 */
                //根据方法名获取方法对应的参数列表
                List<String> params = paramsLoadMap.get(method);
                log.info("当前方法的参数列表为：" + params);
                //如果参数列表为空，则不添加参数加载代码
                if (params != null && params.size() > 0) {
                    for (String param : params) {
                        String loadParam = param + "=joblib.load(" + param.strip() + "_path.path)[\"" + param.strip() + "\"]";
                        //下面两句代码是对其，删除多余空格再加上对齐
                        loadParam = loadParam.strip();
                        loadParam = "    " + loadParam;
                        currentCodes.add(loadParam);
                    }
                }
            } else {//表示不是方法定义语句
                //如果是return语句
                if (code.strip().startsWith("return ")) {
                    String returnValueString = code.strip().replace("return ", "");
                    //返回值的列表
                    List<String> returnValueList = List.of(returnValueString.split(","));
                    //    joblib.dump({"model":model}, output_path.path)
                    StringBuilder dumpReturnValue = new StringBuilder();
                    //获取到返回值对应的元数据名
                    String outputMeta = funcReturnMetaStack.pop();
                    dumpReturnValue.append("    joblib.dump({");
                    String singleParam = "";
                    for (String returnParam : returnValueList) {
                        singleParam += "\"" + returnParam.strip() + "\":" + returnParam.strip() + ",";
                    }
                    dumpReturnValue.append(singleParam);
                    dumpReturnValue.append("}," + outputMeta + ".path)");
                    currentCodes.add(dumpReturnValue.toString());
                } else {
                    currentCodes.add(code);
                }
            }

        }

        /**
         * 到此为止 数据的方法改造完成
         * 下面要做的是方法调用当前代码文件中的其他方法时将其他方法引入到当前的方法中
         */
        List<String> resCodes = addReferency(currentCodes, noChineseCodes, importCodes);


        /**
         * 将代码存入文件并执行
         */
        String fileName = generateCode.getComponentName() + ".py";
        try {
            FileUtils.writeCode(resCodes, fileName);
        } catch (IOException e) {
            e.printStackTrace();
        }
        callPythonFunc("python " + fileName);
        return null;
    }

    /**
     * 添加方法调用方法的转换
     * 还传入了initialcode用来获取被调用方法最开始的样子，在方法内部调用不需要进行方法参数的转换 因此需要初始代码
     *
     * @param codes
     * @return
     */
    @Override
    public List<String> addReferency(List<String> codes, List<String> initialCodes, List<String> importList) {
        //紧凑代码，删除多余的空行
        List<String> list = initialCodes.stream().filter(code -> !StringUtils.isEmpty(code.strip().replaceAll("\n", ""))).collect(Collectors.toList());
        //获取到了每个方法
        HashMap<String, List<String>> funcCodes = generateCode.getFuncCodes(list);
        //构造返回数据列表
        List<String> resList = new LinkedList<>(codes);
        for (Map.Entry<String, List<String>> entry : funcCodes.entrySet()) {
            //  获取当前方法中所调用的函数
            HashSet<String> callMethods = generateCode.getCallMethods(entry.getValue());
            for (String funcName : callMethods) {
                //如果当前方法调用了其他方法，就获取到那个方法并添加到当前方法里面去
                if (funcCodes.get(funcName) != null) {
                    List<String> innerFuncCode = funcCodes.get(funcName).stream().map(e -> "    " + e).collect(Collectors.toList());
                    //遍历所有代码获取到当前方法并在当前方法的下一行添加被调用的代码
                    for (int i = 0; i < codes.size(); i++) {
                        String currentCode = codes.get(i);
                        String currentFuncName = generateCode.getFuncName(currentCode);
                        if (StringUtils.isEmpty(currentFuncName)) {
                            //表示当前代码不是方法定义代码
                            continue;
                        }
                        //如果当前代码是方法定义代码的话,判断是否是当前方法 如果是的话就在当前代码下插入引用方法的代码
                        if (Objects.equals(currentFuncName, entry.getKey())) {
                            //向下探测 直到找到import的最后一句话,将detect探测到不是导包语句的第一行
                            i++;
                            while (codes.get(i).strip().startsWith("import ") || codes.get(i).strip().startsWith("from ")) {
                                i++;
                            }
                            resList.addAll(i, innerFuncCode);
                        }
                    }
                }
            }
        }
        return resList;
    }


    /**
     * 调用python方法
     *
     * @param command
     * @return
     */
    @Override
    public String callPythonFunc(String command) throws IOException, InterruptedException {
        Process p = Runtime.getRuntime().exec(command);
        BufferedReader br = new BufferedReader(new
                InputStreamReader(p.getInputStream()));
        String line = null;
        while ((line = br.readLine()) != null) {
            System.out.println(line);
        }
        br.close();
        p.waitFor();

        return null;
    }
}
