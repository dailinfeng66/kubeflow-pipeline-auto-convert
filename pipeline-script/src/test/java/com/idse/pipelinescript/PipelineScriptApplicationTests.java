package com.idse.pipelinescript;

import com.idse.pipelinescript.service.impl.GenerateScriptImpl;
import com.idse.pipelinescript.utils.generate.code.impl.GenerateCodeImpl;
import com.idse.pipelinescript.utils.generate.code.intf.GenerateCode;
import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

import javax.annotation.Resource;
import java.io.IOException;
import java.util.HashSet;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import static java.util.regex.Pattern.compile;

@SpringBootTest
@Slf4j
class PipelineScriptApplicationTests {

    @Resource
    GenerateCode generateCode;

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
    void readFileTest() throws IOException, InterruptedException {
        String filpath = "/Users/dailinfeng/Desktop/实验室项目/kubeflow/pipeline-script/src/main/resources/testfile.py";

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
        System.out.println(generateCode.getFuncName("def fun2_min(params=10, x:int=10, y)"));
        System.out.println(generateCode.getFuncName("    def fun2_min(params=10, x:int=10, y):"));
    }

    /**
     * 测试根据源码列表获取方法名的set
     */
    @Test
    void getSourceFunc() {
        HashSet<String> sourceFunc = generateCode.getSourceFunc(List.of(
                "def load_data(url,filename:str,url1:int = 10):",
                "    f = requests.get(url)",
                "def get_model1(xdata,ydata):"
        ));
        System.out.println(sourceFunc);
    }
}
