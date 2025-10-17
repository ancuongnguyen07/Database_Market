## Quantitive study of Database marketplace
This study is the final research project which is a part of COMP.SEC.400 Digital Privacy course provided by Tampere Universiy.

Database market is a dark marketplace which is hosted in the Tor network.
In this study, I explored the price distribution of all products in this dark marketplace and allocation of product types.

A full report (LaTeX source) at [report](./report/).
Run the following commands to build the PDF final report.
```
$ cd ./report
$ make
```

*Cannot build the report?*. The final report is available [here](./report/report.pdf)

### Replicate the results of study
If you already got the dataset, you can skip to step 4.
1. Download the dataset at [this link](https://mega.nz/folder/aJwVyIYJ#9SWh-Z3-TpPfjHZeFxbeew)
2. Check the SHA256 checksum: **a5f2cb4feb7fee597b0a26b1dc2fb33b1f9cae639e995a89663198bcfa76f1a**
3. Extract the compressed dataset
    ```
    $ tar -xf database.tar.gz
    ```
4. Run the following commands
    ```
    $ python data_featuring.py
    $ python data_analysis.py
    $ python data_visualization.py
    ```
5. All generated files are stored in the folder `analysis_result`

### Copyright
The original dataset is given by Juha Nurmi, the responsible teacher of the course. Check the the copyright at [README.md](https://mega.nz/folder/aJwVyIYJ#9SWh-Z3-TpPfjHZeFxbeew)
