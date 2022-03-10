package com.idse.pipelinescript;

import com.idse.pipelinescript.service.impl.GenerateScriptImpl;
import com.idse.pipelinescript.utils.FileUtils;
import com.idse.pipelinescript.utils.generate.code.intf.GenerateCode;
import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.util.StringUtils;

import javax.annotation.Resource;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
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
        List<String> list = codeLines.stream().filter(code -> !StringUtils.isEmpty(code.strip().replaceAll("\n", ""))).collect(Collectors.toList());
        //获取到了每个方法
        HashMap<String, List<String>> funcCodes = generateCode.getFuncCodes(list);
        log.info(funcCodes.keySet().toString());
        for (Map.Entry<String, List<String>> entry : funcCodes.entrySet()) {
            //当前方法名
            String funcCurrentFuncName = entry.getKey();
            //  获取当前方法中所调用的函数
            HashSet<String> callMethods = generateCode.getCallMethods(entry.getValue());
            log.info(callMethods.toString());
            for (String funcName : callMethods) {
                //如果当前方法调用了其他方法，就获取到那个方法并添加到当前方法里面去
                if (funcCodes.get(funcName) != null) {
                    List<String> innerFuncCode = funcCodes.get(funcName).stream().map(e -> "    " + e).collect(Collectors.toList());
                    entry.getValue().addAll(1, innerFuncCode);
                }
            }
        }

    }

    @Test
    void getCallFunc() {
//        generateCode.getCallMethods("    fun1min(fun2min,model - y)");
    }

}
