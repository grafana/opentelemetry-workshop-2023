package com.grafana.otelworkshop.springboot;

import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;

/**
 * Handle requests to https://localhost:4321/
 */
@RestController
public class AppController {
    
    @RequestMapping("/")
    public String home() {
        return "ok";
    }
}
