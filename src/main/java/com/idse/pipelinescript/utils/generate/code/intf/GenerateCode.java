package com.idse.pipelinescript.utils.generate.code.intf;

import com.idse.pipelinescript.pojo.pipeline.Component;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;

/**
 * @Author dailinfeng
 * @Description TODO
 * @Date 2022/3/2 10:49 AM
 * @Version 1.0
 */
@org.springframework.stereotype.Component
public interface GenerateCode {
    /**
     * 获取不带数字不带中划线的UUID
     *
     * @return
     */
    String getComponentName();

    /**
     * 将组件列表转为Map 并添加随机返回变量名
     *
     * @param components
     * @return
     */
    Map<String, Component> getComponentMap(List<Component> components);

    /**
     * 检测一个字符串是否含有中文
     *
     * @param code
     * @return
     */
    boolean containChinese(String code);

    /**
     * 根据import包的语句获取到需要导入的包
     *
     * @param importCodes
     * @return
     */
    List<String> getDependences(List<String> importCodes);

    /**
     * 根据方法定义代码获取方法名
     *
     * @param code
     * @return   如果当前行代码不是方法定义代码的话就返回空
     */
    String getFuncName(String code);

    /**
     * 检测一个传入的代码中有哪一些是方法并返回方法名
     *
     * @param codes
     * @return
     */
    HashSet<String> getSourceFunc(List<String> codes);

    /**
     * 获取一个方法中调用外部方法的方法名
     *
     * @param codes
     * @return
     */
    HashSet<String> getCallMethods(List<String> codes);

    /**
     * 获取一个方法的所有代码
     *      返回结果是一个Map
     *          key：方法名
     *          value：方法的代码
     * @param codes
     * @return
     */
    HashMap<String,List<String>> getFuncCodes(List<String> codes);
}
