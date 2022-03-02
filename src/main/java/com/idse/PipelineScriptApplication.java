package com.idse;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.servlet.config.annotation.EnableWebMvc;
import springfox.documentation.swagger2.annotations.EnableSwagger2;

/**
 * @author dailinfeng
 */
@SpringBootApplication
@EnableSwagger2
@EnableWebMvc
public class PipelineScriptApplication {

    public static void main(String[] args) {
        SpringApplication.run(PipelineScriptApplication.class, args);
    }

}
