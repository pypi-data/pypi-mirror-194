# Title     : LFMM
# Objective : run lfmm by using kmers selected randomly
# Created by: Julie Orjuela UMR DIADE IRD
# Created on: 20/10/2022

#### Loading required packages #####
suppressPackageStartupMessages(library("optparse"))
suppressPackageStartupMessages(library(Biostrings))

#### COMMAND LINE ARGUMENTS PARSING ######
option_list <- list(
  make_option(c("-e", "--bedFile"),
              type = "character",
              default = NULL,
              help = "Path of bed file"),
  make_option(c("-i", "--bimFile"),
              type = "character",
              default = NULL,
              help = "Path of bim file"),
  make_option(c("-a", "--famFile"),
              type = "character",
              default = NULL,
              help = "Path of fam file"),
  make_option(c("-o", "--outFilePath"),
              type = "character",
              default = NULL,
              help = "Path where output sequence file will be written."),
  make_option(c("-k", "--kmerList"),
              type = "character",
              default = NULL,
              help = "kmer list"),
  make_option(c("-p", "--phenoFile"),
              type = "character",
              default = NULL,
              help = "phenotype file"),
  make_option(c("-x", "--pcaAxes"),
              type = "integer",
              default = 2,
              help = "axes in PCA, 2 by default"),
  make_option(c("-c", "--correction"),
              type = "character",
              default = "FDR",
              help = "correction method to extrac kmers outliers"),
  make_option(c("-f", "--alpha"),
              type = "double",
              default = 0.1,
              help = "alpha cutoff for outlier detection")
)

##### RETRIEVEING PARAMS from optparse #####
myArgs <- parse_args(
  OptionParser(usage = "%prog [options]", option_list = option_list,
               description = "run LFMM R package over a subset of random kmers and a bed+bim+fam file"))

# assign parameter values
bed <- myArgs$bedFile
bim <- myArgs$bimFile
fam <- myArgs$famFile
out <- myArgs$outFilePath
kmer_list <- myArgs$kmerList
phenotype_file <- myArgs$phenoFile
nb_axes_pca <- myArgs$pcaAxes
correction <- myArgs$correction
alpha <- myArgs$alpha

# controling parametters
if(is.null(out)) out <- paste0(gsub("(^.*)\\..*$", "\\1", bedFile), "_lfmm.csv")
if (is.null(bed)) stop("bed file must be provided. Run program with '--help' for more info on usage.")
if (is.null(bim)) stop("bim file must be provided. Run program with '--help' for more info on usage.")
if (is.null(fam)) stop("fam file must be provided. Run program with '--help' for more info on usage.")
if (is.null(phenotype_file)) stop("give phenotype file file to lfmm. Run program with '--help' for more info on usage.")

# loading R packages
library("BEDMatrix")
library("lfmm")
library("rlist")
library("stringr")
library('qvalue')

set.seed(802)

# reading samples file from FAM file
file_to_pop = read.delim(fam, sep = ' ', header = FALSE)
# get nb of samples from samples.txt
nb_samples = length(file_to_pop[[1]])

############# phenotype ##############"
# le phenotype est la matrice zscores pour les ind qui avaient des donnes phenotypiques disponibles
phenotype = read.delim(phenotype_file, sep = '\t', header = TRUE)
#print(phenotype[,1])
#print(phenotype)
phenotype = na.omit(phenotype)
#print(phenotype)

print(alpha)
print(nb_axes_pca)
print(correction)

############# genotype ##############
# les genotypes correspond à la table de presence/absence des kmers
# create a BEDMatrix object the example .bed file
bed <- BEDMatrix(bed, simple_names = T)
# extraction of random kmers found in segment file
kl <- scan(kmer_list)

# reduction de la matrix bedmatrix
##genotype <- bed[which(rownames(bed) %in% rownames(phenotype)), sort(kl)]
genotype = bed[1:nb_samples, sort(kl)]
genotype_reduit = genotype[which(rownames(genotype) %in% phenotype[,1]),]

############# LFMM ##############
#The ridge_lfmm function returns an object that contains the latent variable score matrix U,
#the latent variable loading matrix U, and B the effect sizes for all SNPs.
#The result can
# be used to perform an association study:
#print (phenotype[,2])
mod.lfmm <- lfmm_ridge(Y = genotype_reduit, X = phenotype[,2], K = nb_axes_pca)
asso.lffm <- lfmm_test(Y = genotype_reduit, X = phenotype[,2], lfmm = mod.lfmm, calibrate = "gif")

pvalues <- asso.lffm$calibrated.pvalue
#print ("=============== pvalues=============")
###print (head(pvalues))
###scores <- asso.lffm$score
#attributes(mod.lfmm)
#print(head(mod.lfmm$B)) # kmers sequences are here

## Choosing a cutoff for outlier detection
if (correction == 'BONFERONNI')
  {
  ## E.3. Bonferroni correction
  padj <- p.adjust(pvalues, method="bonferroni")
  alpha <- alpha
  outliers <- which(padj < alpha)
  }
if (correction == 'BH') {
  ## E.2. Benjamini-Hochberg Procedure
  padj <- p.adjust(pvalues, method="BH")
  #print (head(padj))
  alpha <- alpha
  outliers <- which(padj < alpha)
}
if (correction == 'FDR') {
  ## E.1. q-values
  qval <- qvalue(pvalues)$qvalues
  alpha <- alpha
  outliers <- which(qval < alpha)
  ### Error in smooth.spline(lambda, pi0, df = smooth.df) :
  ### missing or infinite values in inputs are not allowed
  ### Calls: qvalue -> pi0est -> smooth.spline
}

###print("================outliers==============")
###print(head(outliers))
## RELATED TO scan(kmer_list) => its not same kmer_number of .bim
#[1]  16  74  90  99 110 195

###print("===============MOD lffm==================")
# recovery kmers sequence by using index
###print(head(mod.lfmm$B))

###print("===============asso lffm==================")
###outliers_kmers = asso.lffm$B[outliers,]
###print(head(outliers_kmers))

###print("===============pvalues outliers==================")
outliers_kmers = pvalues[outliers,]
###print(head(outliers_kmers))

print("=========le nb de kmers outliers ==================")
print(length(outliers_kmers))
#typeof(outliers_kmers)
#attributes(outliers_kmers)

############# preparation ##############"
#### preparing bed name, segment id and names of outfiles files

# finding suffix of _outliers.csv file
short_segment_name = sub(pattern = "(.*)_lfmm_outliers.csv", replacement = "\\1", basename(out))
ss = str_split(short_segment_name, "_")
short_bed_name = paste (ss[[1]][1],"_",ss[[1]][2], sep = "")
segment_nb = ss[[1]][3]

# getting a output name to rescue pvalues and scores
#filepvalues = str_replace(out, "_outliers.csv", "_outliers.csv")

# doing a vector including original file bed and segment name
filename_vector = rep(c(short_bed_name),times=(length(outliers)))
segment_vector = rep(c(segment_nb),times=(length(outliers)))

# doing a dataframe containing the sequence of kmer and file origin as well as pvalues info, use to output
#df = data.frame(filename_vector, segment_vector, outliers, outliers_kmers )
df = data.frame(filename_vector, segment_vector, outliers_kmers)
names(df) <- NULL

print("=========DF to csv ==================")
print(head(df))

write.table(df, out, quote = FALSE, sep="\t")

# Screen plot
fileplot <- str_replace(out, "_outliers.csv", ".rplot.pdf")
pdf(file=fileplot)
qqplot(rexp(length(pvalues), rate = log(10)),
       -log10(pvalues), xlab = "Expected quantile",
       pch = 19, cex = .4)
abline(0,1)

## Manhattan plot with causal loci shown
plot(-log10(pvalues), pch = 19,
     cex = .2, col = "grey", xlab = "KMER")
dev.off()
