package com.idse.pipelinescript.controller;

import com.idse.pipelinescript.pojo.pipeline.Pipeline;
import com.idse.pipelinescript.response.ResponseData;
import com.idse.pipelinescript.service.intf.GenerateScriptService;
import com.idse.pipelinescript.utils.ResponseDataUtil;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import javax.annotation.Resource;

import java.io.IOException;


/**
 * @Author dailinfeng
 * @Description TODO
 * @Date 2022/2/26 9:39 AM
 * @Version 1.0
 */
@RestController
@CrossOrigin
@Api(tags = "脚本")
public class GenerateScriptController {

    @Resource
    GenerateScriptService generateScriptService;


    @PostMapping("/yaml")
    @ApiOperation("创建pipeline")
    public ResponseData generatePipeline(@RequestBody Pipeline pipeline) throws IOException {
        return ResponseDataUtil.buildSuccess(generateScriptService.generateYaml(pipeline));
    }
}
