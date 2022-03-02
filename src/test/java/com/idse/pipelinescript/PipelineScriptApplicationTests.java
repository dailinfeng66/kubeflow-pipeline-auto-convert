package com.idse.pipelinescript;

import com.idse.pipelinescript.service.impl.GenerateScriptImpl;
import com.idse.pipelinescript.service.intf.GenerateScriptService;
import com.idse.pipelinescript.utils.FileUtils;
import com.idse.pipelinescript.utils.GenerateCode;
import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

import javax.annotation.Resource;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

import static java.util.regex.Pattern.compile;

@SpringBootTest
@Slf4j
class PipelineScriptApplicationTests {

    @Test
    void regularExpression() {
        String code = "def fun2_min(params=10, x:int=10, y):";
        Pattern methodName = compile("^def[ ]{1,}[0-9a-zA-Z_ ]*"); //匹配到定义方法和方法名
        Matcher methodM = methodName.matcher(code);
        methodM.find();
        methodM.group().replaceAll("def ", "").strip();
        System.out.println();
    }

    @Resource
    GenerateScriptImpl generateScriptService;

    @Test
    void readFileTest() {
        String filpath = "/Users/dailinfeng/Desktop/实验室项目/kubeflow/pipeline-script/src/main/resources/envtest.py";

        generateScriptService.generateComponent(filpath);
    }

    @Test
    void pattern() {
        String param = "xdata";
        //匹配参数名字，因为名字里还有默认值那些
        Pattern variableName = compile("^[0-9a-zA-Z_ ]*");
        Matcher paramM = variableName.matcher(param.strip());
        System.out.println(paramM.find());
        System.out.println(paramM.group());
    }

    @Test
    void codeTest() {
        String code = "    def fun1min(params, x, y):";
        Pattern methodNamePattern = compile("def[ ]{1,}[0-9a-zA-Z_ ]*");
        Matcher methodNameMatchar = methodNamePattern.matcher(code);
        methodNameMatchar.find();
        System.out.println(methodNameMatchar.group());

    }

    /**
     * 测试根据方法定义代码获取方法名
     */
    @Test
    void getFuncName() {
        System.out.println(GenerateCode.getFuncName("def fun2_min(params=10, x:int=10, y)"));
        System.out.println(GenerateCode.getFuncName("    def fun2_min(params=10, x:int=10, y):"));
    }

    /**
     * 测试根据源码列表获取方法名的set
     */
    @Test
    void getSourceFunc() {
        HashSet<String> sourceFunc = GenerateCode.getSourceFunc(List.of(
                "def load_data(url,filename:str,url1:int = 10):",
                "    f = requests.get(url)",
                "def get_model1(xdata,ydata):"
        ));
        System.out.println(sourceFunc);
    }
}
