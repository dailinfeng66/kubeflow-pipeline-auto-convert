package com.idse.pipelinescript.utils.generate.code.impl;


import com.idse.pipelinescript.pojo.pipeline.Component;
import com.idse.pipelinescript.utils.generate.code.intf.GenerateCode;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

import static java.util.regex.Pattern.compile;

/**
 * @Author dailinfeng
 * @Description TODO
 * @Date 2022/2/25 7:36 PM
 * @Version 1.0
 */
@org.springframework.stereotype.Component
@Slf4j
public class GenerateCodeImpl implements GenerateCode {
    /**
     * 获取不带数字不带中划线的UUID
     *
     * @return
     */
    @Override
    public String getComponentName() {
        return UUID.randomUUID().toString().replaceAll("-", "_").replaceAll("\\d+", "");
    }

    /**
     * 将组件列表转为Map 并添加随机返回变量名
     *
     * @param components
     * @return
     */
    @Override
    public Map<String, Component> getComponentMap(List<Component> components) {
        Map<String, Component> hashMap = new HashMap<>();
        for (Component component : components) {
            component.setResValueName(getComponentName());
            hashMap.put(component.getId(), component);
        }
        return hashMap;
    }

    /**
     * 检测一个字符串是否含有中文
     *
     * @param code
     * @return
     */
    @Override
    public boolean containChinese(String code) {
        Pattern p = compile("[\u4E00-\u9FA5|\\！|\\，|\\。|\\（|\\）|\\《|\\》|\\“|\\”|\\？|\\：|\\；|\\【|\\】]");
        Matcher m = p.matcher(code);
        if (m.find()) {
            return true;
        }
        return false;
    }


    /**
     * 根据import包的语句获取到需要导入的包
     *
     * @param importCodes
     * @return
     */
    @Override
    public List<String> getDependences(List<String> importCodes) {
        List<String> dependences = importCodes.parallelStream().map(code -> {
            code = code.strip();
            String dependency = "";
            //import XXX 型
            if (code.startsWith("import ")) {
                Pattern dependencyPattern = compile("^import[ ]{1,}[0-9a-zA-Z]*");
                Matcher dependencyMatcher = dependencyPattern.matcher(code);
                dependencyMatcher.find();
                dependency = dependencyMatcher.group();
                dependency = dependency.replace("import ", "").strip();

            }
            //from xxx import xxx型
            if (code.startsWith("from ")) {
                Pattern dependencyPattern = compile("^from[ ]{1,}[0-9a-zA-Z]*");
                Matcher dependencyMatcher = dependencyPattern.matcher(code);
                dependencyMatcher.find();
                dependency = dependencyMatcher.group();
                dependency = dependency.replace("from ", "").strip();
            }
            return "\'" + dependency + "\'";
        }).collect(Collectors.toList());
        return new ArrayList<>(new HashSet<>(dependences));
    }

    /**
     * 根据方法定义代码获取方法名
     *
     * @param code
     * @return
     */
    @Override
    public String getFuncName(String code) {
        //def fun2_min(params=10, x:int=10, y): ---> fun2_min
        code = code.strip();
        if (!code.startsWith("def ") || !code.strip().endsWith(":")) {
            return null;
        }
        Pattern methodName = compile("^def[ ]{1,}[0-9a-zA-Z_ ]*");
        Matcher methodM = methodName.matcher(code.strip());
        if (methodM.find()) {
            String funcName = methodM.group();
            return funcName.replaceAll("def", "").strip();
        }
        return null;
    }

    /**
     * 检测一个传入的代码中有哪一些是方法并返回方法名
     *
     * @param codes
     * @return
     */
    @Override
    public HashSet<String> getSourceFunc(List<String> codes) {
        HashSet<String> hashSet = new HashSet<>();
        for (String code : codes) {
            String funcName = getFuncName(code);
            if (funcName != null) {
                hashSet.add(funcName);
            }
        }
        return hashSet;
    }

    /**
     * 获取一个方法的所有变量
     *
     * @param codes
     * @return
     */
    @Override
    public HashSet<String> getVariable(List<String> codes) {
        HashSet<String> hashSet = new HashSet<>();
        for (String code : codes) {
            //去除前后空格
            code = code.strip();

        }
        return null;
    }

    /**
     * 获取一个方法的所有代码
     * 返回结果是一个Map
     * key：方法名
     * value：方法的代码
     *
     * @param codes
     * @return
     */
    @Override
    public HashMap<String, List<String>> getFuncCodes(List<String> codes) {
        HashMap<String, List<String>> hashMap = new HashMap<>();
        List<String> codeList = null;
        //当前方法的标记
        String funcName = "";
        for (String code : codes) {
            //如果当前代码是方法的定义代码
            if (code.strip().startsWith("def ") && code.strip().endsWith(":")) {
                //表示前一个方法已结束 因为已经碰到了下一个方法的方法定义代码
                if (codeList != null && !StringUtils.isEmpty(funcName)) {
                    //存储当前方法的代码
                    hashMap.put(funcName, codeList);
                }
                //获取方法名
                funcName = getFuncName(code);
                //重新初始化方法列表
                codeList = new LinkedList<>();
                codeList.add(code);
            } else {
                //如果当前代码属于一个方法
                if (!StringUtils.isEmpty(funcName) && codeList != null) {
                    codeList.add(code);
                }
            }
        }
        //添加最后一个方法
        if (!StringUtils.isEmpty(funcName)) {
            hashMap.put(funcName, codeList);
        }
        return hashMap;
    }
}
