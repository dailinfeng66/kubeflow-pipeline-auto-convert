package com.idse.pipelinescript.utils;

import lombok.extern.slf4j.Slf4j;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

/**
 * @Author dailinfeng
 * @Description TODO
 * @Date 2022/2/28 9:33 AM
 * @Version 1.0
 */
@Slf4j
public class FileUtils {

    /**
     * 按行读取一个源码文件，并以一个list返回
     *
     * @param filepath
     * @return
     */
    public static List<String> readSourceCode(String filepath) {
        FileInputStream inputStream = null;
        BufferedReader bufferedReader = null;
        List<String> codes = new ArrayList<>();
        try {
            inputStream = new FileInputStream(filepath);
            bufferedReader = new BufferedReader(new InputStreamReader(inputStream));
            String line = null;
            while ((line = bufferedReader.readLine()) != null) {
                codes.add(line);
            }
        } catch (IOException e) {
            log.error(e.getMessage());
        } finally {
            try {
                inputStream.close();
                bufferedReader.close();
            } catch (IOException e) {
                log.error(e.getMessage());
            }
        }
        return codes;
    }

    /**
     * 写代码入文件
     *
     * @param codes
     * @param fileName
     * @return
     * @throws IOException
     */
    public static Boolean writeCode(List<String> codes, String fileName) throws IOException {
        BufferedWriter writer = new BufferedWriter(new FileWriter(fileName));
        for (String code : codes) {
            writer.write(code + "\n");
        }

        writer.close();
        return true;
    }
}
