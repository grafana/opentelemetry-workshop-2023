package com.grafana.otelworkshop.springboot;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;

@Configuration
@EnableAutoConfiguration
@ComponentScan
public class App {
  
    public static void main(String[] args) {
        ApplicationContext ctx = SpringApplication.run(App.class, args);    
    }
}
