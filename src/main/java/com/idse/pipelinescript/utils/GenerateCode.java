package com.idse.pipelinescript.utils;


import com.idse.pipelinescript.pojo.pipeline.Component;
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
public class GenerateCode {


    /**
     * 获取不带数字不带中划线的UUID
     *
     * @return
     */
    public static String getComponentName() {
        return UUID.randomUUID().toString().replaceAll("-", "_").replaceAll("\\d+", "");
    }

    /**
     * 将组件列表转为Map 并添加随机返回变量名
     *
     * @param components
     * @return
     */
    public static Map<String, Component> getComponentMap(List<Component> components) {
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
    public static boolean containChinese(String code) {
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
    public static List<String> getDependences(List<String> importCodes) {
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
    public static String getFuncName(String code) {
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
    public static HashSet<String> getSourceFunc(List<String> codes) {
        HashSet<String> hashSet = new HashSet<>();
        for (String code : codes) {
            String funcName = getFuncName(code);
            if (funcName != null) {
                hashSet.add(funcName);
            }
        }
        return hashSet;
    }
}
