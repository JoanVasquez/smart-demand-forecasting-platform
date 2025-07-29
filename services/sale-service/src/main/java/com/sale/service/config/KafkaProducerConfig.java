package com.sale.service.config;
import com.smartforecast.schemas.SaleCreated;
import io.confluent.kafka.serializers.AbstractKafkaSchemaSerDeConfig;
import io.confluent.kafka.serializers.KafkaAvroSerializer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.common.serialization.StringSerializer;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.core.DefaultKafkaProducerFactory;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.core.ProducerFactory;

import java.util.Map;
import java.util.Optional;

@Configuration
public class KafkaProducerConfig {

    @Value("${spring.kafka.bootstrap-servers:}")
    private String bootstrapServers;

    @Value("${spring.kafka.properties.schema.registry.url:}")
    private String schemaRegistryUrl;

    private String requireNonBlank(String value, String name) {
        return Optional.ofNullable(value)
                .filter(s -> !s.isBlank())
                .orElseThrow(() -> new IllegalArgumentException(name + " must not be null or blank"));
    }

    @Bean
    public ProducerFactory<String, SaleCreated> producerFactory() {
        String validBootstrap = requireNonBlank(bootstrapServers, "Kafka bootstrap servers");
        String validSchemaUrl = requireNonBlank(schemaRegistryUrl, "Kafka schema registry URL");

        Map<String, Object> config = Map.of(
                ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, validBootstrap,
                AbstractKafkaSchemaSerDeConfig.SCHEMA_REGISTRY_URL_CONFIG, validSchemaUrl,
                ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class,
                ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, KafkaAvroSerializer.class
        );

        return new DefaultKafkaProducerFactory<>(config);
    }

    @Bean
    public KafkaTemplate<String, SaleCreated> kafkaTemplate() {
        return new KafkaTemplate<>(producerFactory());
    }
}
