package com.idse.pipelinescript;

import com.idse.pipelinescript.service.impl.GenerateScriptImpl;
import com.idse.pipelinescript.utils.FileUtils;
import com.idse.pipelinescript.utils.generate.code.intf.GenerateCode;
import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.Test;
import org.junit.platform.commons.util.StringUtils;
import org.springframework.boot.test.context.SpringBootTest;

import javax.annotation.Resource;
import java.util.HashMap;
import java.util.List;
import java.util.stream.Collectors;

/**
 * @Author dailinfeng
 * @Description TODO
 * @Date 2022/3/2 11:24 AM
 * @Version 1.0
 */
@SpringBootTest
@Slf4j
public class PipelineTest2 {
    @Resource
    GenerateScriptImpl generateScriptService;

    @Resource
    GenerateCode generateCode;
    @Test
    void getFuncCode() {
        String filpath = "/Users/dailinfeng/Desktop/实验室项目/kubeflow/pipeline-script/src/main/resources/testfile.py";
        //读取代码
        List<String> codeLines = FileUtils.readSourceCode(filpath);
        //紧凑代码，删除多余的空行
        List<String> list = codeLines.stream().filter(code -> StringUtils.isNotBlank(code.strip().replaceAll("\n", ""))).collect(Collectors.toList());
        //获取到了每个方法
        HashMap<String, List<String>> funcCodes = generateCode.getFuncCodes(list);


    }
}
