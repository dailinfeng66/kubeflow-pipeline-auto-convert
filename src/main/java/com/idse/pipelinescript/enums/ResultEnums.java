package com.idse.pipelinescript.enums;


/**
 * @author dailinfeng
 */

public enum ResultEnums {
    //成功
    SUCCESS("200", "请求成功"),
    //失败
    ERROR("1111", "请求失败"),
    //系统异常
    SYSTEM_ERROR("1000", "系统异常"),


    ;
    private String code;
    private String msg;

    ResultEnums(String code, String msg) {
        this.code = code;
        this.msg = msg;
    }

    public String getCode() {
        return code;
    }

    public void setCode(String code) {
        this.code = code;
    }

    public String getMsg() {
        return msg;
    }

    public void setMsg(String msg) {
        this.msg = msg;
    }
}