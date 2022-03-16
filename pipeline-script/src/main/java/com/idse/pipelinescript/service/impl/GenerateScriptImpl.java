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
        String saveFilePath = " /Users/dailinfeng/Desktop/实验室项目/kubeflow/pipeline-script/src/main/resources/components/res.py";
        StringBuilder command = new StringBuilder("python src/main/java/com/idse/pipelinescript/python/generate_ast.py ");
        //需要转换的文件的文件位置
        command.append(filePath + " ");
        command.append(saveFilePath);
        System.out.println(command.toString());
        String res = callPythonFunc(command.toString());
        callPythonFunc("python " + saveFilePath);
        System.out.println(res);
        return null;
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
        StringBuilder res = new StringBuilder();
        while ((line = br.readLine()) != null) {
            System.out.println(line);
            res.append(line);
        }
        br.close();
        p.waitFor();
        return res.toString();
    }
}
