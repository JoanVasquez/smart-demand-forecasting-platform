package com.sale.service.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;
import lombok.*;

import java.time.LocalDate;
import java.util.UUID;

@Entity
@Table(name = "tbl_sale")
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class Sale {

    @GeneratedValue(strategy = GenerationType.UUID)
    @Id
    private UUID id;

    @NotNull
    @Column(nullable = false)
    private String productId;

    @NotNull
    @Column(nullable = false)
    private Integer quantity;

    @NotNull
    @Column(nullable = false)
    private LocalDate saleDate;

}
