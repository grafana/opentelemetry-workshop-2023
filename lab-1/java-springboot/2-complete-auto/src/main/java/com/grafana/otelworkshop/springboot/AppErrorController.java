package com.grafana.otelworkshop.springboot;

import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.boot.web.servlet.error.ErrorController;

/**
 * Handle requests to https://localhost:4321/error
 */
@RestController
public class AppErrorController implements ErrorController {
    
    @RequestMapping("/error")
    public String error() {
        return String.valueOf(0/0);
    }
}
