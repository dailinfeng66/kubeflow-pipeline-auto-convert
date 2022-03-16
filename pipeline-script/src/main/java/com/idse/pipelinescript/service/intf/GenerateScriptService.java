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

    String generateComponent(String filePath) throws IOException, InterruptedException;

    /**
     * 调用python方法
     * @param command
     * @return
     */
    String callPythonFunc(String command) throws IOException, InterruptedException;
}
