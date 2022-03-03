package com.idse.pipelinescript.service.intf;

import com.idse.pipelinescript.pojo.pipeline.Pipeline;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.util.List;

/**
 * @Author dailinfeng
 * @Description TODO
 * @Date 2022/2/26 9:40 AM
 * @Version 1.0
 */
@Service
public interface GenerateScriptService {
    boolean generateYaml(Pipeline pipeline) throws IOException;

    String generateComponent(String filePath);

    /**
     * 添加方法调用方法的转换
     *
     * @param codes
     * @return
     */
    List<String> addReferency(List<String> codes, List<String> initialCodes);
}
