package com.sale.service.service;

import com.sale.service.dto.SaleDTO;
import com.sale.service.entity.Sale;
import com.sale.service.exception.NotFoundException;
import com.sale.service.kafka.SaleProducer;
import com.sale.service.repository.SaleRepository;
import com.smartforecast.schemas.SaleCreated;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

@Service
@AllArgsConstructor
public class SaleService {

    private final SaleRepository saleRepository;
    private final SaleProducer saleProducer;

    public Sale createSale(SaleDTO saleDTO) {
        LocalDate localDate = LocalDate.now();
        Sale newSale = Sale.builder().productId(saleDTO.getProductId()).quantity(saleDTO.getQuantity()).saleDate(localDate).build();
        SaleCreated saleCreated = new SaleCreated();
        Sale sale = saleRepository.save(newSale);
        saleCreated.setSaleId(sale.getId().toString());
        saleCreated.setQuantity(sale.getQuantity());
        saleCreated.setProductId(sale.getProductId());
        saleCreated.setSaleDate(sale.getSaleDate().toString());
        saleProducer.publish(saleCreated);
        return sale;
    }

    public List<Sale> listSale() {
       return saleRepository.findAll();
    }

    public Sale getSaleById(UUID id) {
        return saleRepository.findById(id).orElseThrow(() -> new NotFoundException("error while getting the salary by ID"));
    }
}
