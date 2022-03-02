package com.idse.pipelinescript.pojo.pipeline;

import lombok.Data;
import lombok.experimental.Accessors;

/**
 * @Author dailinfeng
 * @Description TODO
 * @Date 2022/2/25 4:06 PM
 * @Version 1.0
 */
@Data
@Accessors(chain = true)
public class Param {
    String name;
    String type;
    String defaultValue;
}
