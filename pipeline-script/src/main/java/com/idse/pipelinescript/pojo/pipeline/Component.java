package com.idse.pipelinescript.pojo.pipeline;

import com.idse.pipelinescript.pojo.pipeline.ComponentInputParam;
import lombok.Data;
import lombok.experimental.Accessors;

import java.util.ArrayList;
import java.util.List;

/**
 * @Author dailinfeng
 * @Description TODO
 * @Date 2022/2/25 4:07 PM
 * @Version 1.0
 */
@Data
@Accessors(chain = true)
public class Component {
    String name;
    String id;
    String url;
    String funcName;
    List<ComponentInputParam> componentInputParams = new ArrayList<>();
    String resValueName;
}
