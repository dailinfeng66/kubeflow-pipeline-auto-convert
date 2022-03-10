package com.idse.pipelinescript.pojo.pipeline;

import lombok.Data;
import lombok.experimental.Accessors;

/**
 * @Author dailinfeng
 * @Description TODO
 * @Date 2022/2/25 4:08 PM
 * @Version 1.0
 */
@Data
@Accessors(chain = true)
public class ComponentInputParam {
    public String name; //参数名字
    public String originCompoId; //上一步组件的id
    public Boolean pipelineParam = false; //是否是pipeline方法参数
    public String pipelineParamName; //pipelineParam 为true时填写
}
