# conorm

**conorm** (stands for "count normalization") implements simple normalization techniques that are frequently used in the analysis of RNA expresison data. The true purporse of this package is to make a pythoneer bioinformatician workflow less colluded with *R*. Currently impleneted methods are

 - Trimmed Means of M-values (*TMM*): this approach is used by **edgeR** by default. The method [is due to MD Robinson](https://genomebiology.biomedcentral.com/articles/10.1186/gb-2010-11-3-r25) (`tmm`, `tmm_norm_factors`);
 - Total count normalization (`total_count`);
 - Counts Per Million (*CPM*) aka "total count normalization multiplied by a million" (`cpm`);
 - Reads Per Kilobase (*RPK*) (`rpk`, note that gene lengths must be provided);
 - Reads Per Kilobase per Million (*RPKM*): RPK multiplied by a million (`rpkm`);
 - GeTMM that is effectivelly RPK + TMM, the approach is [by Marcel Smid et al.](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-018-2246-7) (`getmm`);
 - Percentile normalization (`percentile`);
 - Quartile normalization (as a wrapper around the previous) (`quartile`);

Of course, the sole reason to use **conorm** is its TMM implementation.


## Usage example

We use randomly generated count matrix for simplicity:

```
import conorm
from pandas import read_csv

df = read_csv('test_data/sample.csv', index_col=0)
df_tmm = conorm.tmm(df)
```

The `tmm` method can also return normalization factors if a user specifies `return_norm_factors=True` argument. Optionally, if one doesn't want to normalize data immediately with TMM, but merely want to obtain norm factors, one can use method `tmm_norm_factors`:
```
nf  = tmm_norm_factors(df)
```

An expected result:
```
                             norm.factors
mouse1_lib1.final_cell_0219      1.513987
mouse1_lib3.final_cell_0027      0.697493
mouse1_lib3.final_cell_0218      1.682216
mouse2_lib1.final_cell_0176      0.550935
mouse2_lib1.final_cell_0219      1.249748
mouse2_lib1.final_cell_0222      0.815294
mouse2_lib2.final_cell_0213      0.942643
mouse2_lib2.final_cell_0280      1.154704
mouse2_lib3.final_cell_0242      0.726503
mouse2_lib3.final_cell_0244      1.268131
```

This can be further used to be fed into most of the other methods, e.g. `cpm`:
```
df_tmm_cpm = conorm.cpm(df, norm_factors=nf)
```

All functions are very simple and have docstrings attached, so please see them for extra arguments and documentation on other methods that are not showcased in this readme.

## TODO

Chances are than in a foreseable future Median Rate Normalization (*MRN*) will also be added to the **conorm**.


## Deviations from an edgeR output

A meticulous user might notice that there are some deviations in norm factors produced by **conorm** and **edgeR** with TMM, which are hopefully very small (MSE is to have an order of 1e-3-1e-4). The author shrugs his shoulders, however the chances are that that's due to minor implementation-specific differences at the trimming stage, namely, at the calculation of percentiles.


## Acknowledgement
Surpisingly, there were *mostly* no package in Python that could do TMM to the best of my knowledge until now. However, there were some past work that I should acknowledge that was done previously by a good friend of mine:
[**pyGMNormalize**](https://github.com/ficusss/PyGMNormalize) (Grigory Feoktistov). Unfortunately, the project produced results far off from the **edgeR** due to both implementation errors and the lack of centering of norm. factors by their geometric means. The author displayed lack of desire to correct for those issues and the project is not maintained any longer. Nevertheless, without Grigory's past attempt at solving this trivial task I would never realise that it is that easy indeed and **conorm** would never be born.
