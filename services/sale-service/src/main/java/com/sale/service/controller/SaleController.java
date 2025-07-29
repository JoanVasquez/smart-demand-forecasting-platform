package com.sale.service.controller;

import com.sale.service.dto.SaleDTO;
import com.sale.service.entity.Sale;
import com.sale.service.service.SaleService;
import jakarta.validation.Valid;
import lombok.AllArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/v1/sale")
@AllArgsConstructor
public class SaleController {

    private final SaleService saleService;

    @PostMapping
    public ResponseEntity<Sale> createSale(@Valid @RequestBody SaleDTO saleDTO) {
        return new ResponseEntity<>(saleService.createSale(saleDTO),HttpStatus.CREATED);
    }

    @GetMapping
    public ResponseEntity<List<Sale>> getSales() {
        return new ResponseEntity<>(saleService.listSale(), HttpStatus.OK);
    }

    @GetMapping("/{id}")
    public ResponseEntity<Sale> getSaleById(@PathVariable(name = "id") UUID id) {
        return new ResponseEntity<>(saleService.getSaleById(id), HttpStatus.OK);
    }
}
