package com.idse.pipelinescript.pojo.pipeline;

import lombok.Data;
import lombok.experimental.Accessors;

import java.util.ArrayList;
import java.util.List;

/**
 * @Author dailinfeng
 * @Description TODO
 * @Date 2022/2/25 4:03 PM
 * @Version 1.0
 */
@Data
@Accessors(chain = true)
public class Pipeline {
    /**
     * pipeline的名字
     */
    String pipelineName;
    /**
     * 对这个pipeline的描述
     */
    String description;
    /**
     * 定义pipeline的方法名
     */
    String pipelineFuncName;
    /**
     * pipeline方法的参数
     */
    List<Param> pipelineParams = new ArrayList<>();
    /**
     * pipeline的组件
     */
    List<Component> components = new ArrayList<>();
}
