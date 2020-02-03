

# Utilizacão

```shell
python -m datasus <subcomando> [opcões]
```

**Subcomandos**
- **download**: obtém arquivos brutos da internet
- **list**: exibe informações sobre os arquivos brutos presentes
- **load**: converte os arquivos brutos para um formato desejado
- **get**: obtém arquivos e converte-os para o formato desejado. Equivalente a chamar "download" e "load" em sequência

**Opcões**
- -f: Arquivo de configurações
- -o: Arquivo de saída
- -base: Bases de dados separadas por vírgula, ex.: SIASUS,SIHSUS,...
- -ufs: UFs separadas por vírgula
- -ano: Anos separados por vírgula ou em intervalo, ex.: 2014-2019
