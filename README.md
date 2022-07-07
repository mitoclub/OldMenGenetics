# NGS analysis of oldmen meat mtDNA

## Prequel

Лучше смотреть то, что в папке trimmed (триммил fastp, так как она хорошо отрезает полиG с концов прочтений, которые в большом количестве генерирует новасек)

На всяк, вызывал так:

```bash
for infile in *.R1.fastq.gz
  do
    base=$(basename ${infile} .R1.fastq.gz)
    fastp -i ${base}.R1.fastq.gz -o ${base}.trimmed.R1.fastq.gz -I ${base}.R2.fastq.gz -O ${base}.trimmed.R2.fastq.gz -z 7 -V -g --poly_g_min_len 5 -x --poly_x_min_len 10 -5 -3 -M 25 -n 3 -e 20 -l 77 -c -w 12
  done
```

Картирование показало, что как бэ... - мтДНК не суперчистая - на референс (взял два сэмпла) картируется 3-5% ридов. По этой причине и итоговое покрытие картирования не айс, в районе 50x, хотя по количеству исходных ридов должно быть под 800х

Как-то так.

## Workflow

### Contents

1. [QC](#QC)
2. [Mapping](#Mapping)
3. ...

### QC

```bash
cd data/interim/trimmed && mkdir qc && fastqc *.fastq.gz -o qc -t 24 && multiqc -o qc/multi --title trimmed qc && cd -
```

### Mapping

```bash
bwa index data/interim/mapping/ref/NC_012920.1.fasta
# $BWAPATH bwasw -t $THREADS $REF $SAMPLE | $SAMTOOLSPATH view -h -f 0 -F 256 -@ $THREADS > "$SAMPLE.sam"

for r1 in data/interim/trimmed/Kgd-mtDNA-S*.trimmed.R1.fastq.gz
  do 
    r2=${r1/R1/R2}
    # bn=`basename $r1`
    # lbl=(${bn//./ })
    lbl=`basename $r1 ".trimmed.R1.fastq.gz"`
    echo $lbl
    bwa mem -t 24 data/interim/mapping/ref/NC_012920.1.fasta $r1 $r2 | samtools sort -O bam > data/interim/mapping/${lbl}.bam
  done
```

### Mapping stats

```bash
for bam in data/interim/mapping/Kgd-mtDNA-S*.bam
  do
    basename $bam '.bam'
    samtools flagstat $bam -O tsv | grep "mapped %"
    echo
  done
```

### Depth

```bash
samtools depth -H -q 20 data/interim/mapping/*.bam > data/interim/depth.tsv
```

## Hints

1. In SNP calling it is a good idea to remove duplicates, as the statistics used in the tools that call SNPs sub-sequently expect this (most tools anyways). However, for other research questions that use mapping, you might not want to remove duplicates, e.g. RNA-seq.
2. ...

## References

1. [fastqc](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/)
2. ...
