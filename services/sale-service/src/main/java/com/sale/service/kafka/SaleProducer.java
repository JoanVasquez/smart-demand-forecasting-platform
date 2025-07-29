package com.sale.service.kafka;

import com.smartforecast.schemas.SaleCreated;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

@Component
public class SaleProducer {
    private final KafkaTemplate<String, SaleCreated> kafkaTemplate;

    @Value("${app.topic.sales-created}")
    private String topic;

    public SaleProducer(KafkaTemplate<String, SaleCreated> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }

    public void publish(SaleCreated sale) {
        kafkaTemplate.send(topic, sale.getSaleId().toString(), sale);
    }
}
