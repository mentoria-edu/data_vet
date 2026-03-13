# Classe ShapefileHandler

## Visão geral

A classe `ShapefileHandler` fornece uma interface para carregar,
manipular e exportar dados de um Shapefile.

Durante a inicialização:

1. O shapefile é carregado usando GeoPandas.
2. O CRS do arquivo é verificado.
3. Os dados são reprojetados para o CRS definido pelo sistema.

Os dados são mantidos internamente em um `GeoDataFrame`.

---

## Diagrama de classes

```mermaid
classDiagram
    direction TB

    class ShapefileHandler {
        -Path _shapefile_path
        -_AllowedOutputCRS _output_crs
        -GeoDataFrame _gdf
        +__init__(shapefile_path: Path, output_crs: _AllowedOutputCRS)
        +change_crs(output_crs: _AllowedOutputCRS)
        +to_geodataframe()
        +to_geojson()
        +export_geojson(output_path: Path)
        +export_csv(output_path: Path)
    }

    class _AllowedOutputCRS {
        <<enumeration>>
        SIRGAS_2000
        LATLON
        METERS
        +crs()
    }

    class StrEnum
    class Path
    class CRS
    class GeoDataFrame

    _AllowedOutputCRS --|> StrEnum
    ShapefileHandler --> _AllowedOutputCRS
    ShapefileHandler --> Path
    ShapefileHandler --> CRS
    ShapefileHandler --> GeoDataFrame
```

---

## Responsabilidades da classe

- Carregar shapefile
- Validar CRS
- Reprojetar geometria
- Exportar dados

---

## Atributos principais

### `_shapefile_path`

Armazena o caminho do arquivo shapefile de origem.

### `_output_crs`

Armazena o CRS de saída permitido pela regra de negócio.

### `_gdf`

Armazena o GeoDataFrame carregado e normalizado internamente.

---

## Métodos públicos

### `change_crs`

Reprojeta o GeoDataFrame interno para outro CRS permitido.

### `to_geodataframe`

Retorna uma cópia do GeoDataFrame interno.

### `to_geojson`

Serializa os dados para uma string GeoJSON.

### `export_geojson`

Exporta os dados para um arquivo GeoJSON.

### `export_csv`

Exporta os dados para CSV convertendo a geometria para formato WKT.