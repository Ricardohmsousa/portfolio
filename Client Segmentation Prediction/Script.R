  
  # ------------------------------ Clients Limpeza de Dados -----------------------------------------
  
  #dataClients <- read.table(file="D:/MSIC/1Ano/2Semestre/DESCO/Trabalho Repo/DESCO/Trabalho Parte 1/Data/CLIENTS.txt", header = TRUE, sep="\t", stringsAsFactors = TRUE)
   dataClients <- read.table(file="C:/Users/ricar/Desktop/DESCO/desco/Trabalho Parte 1/Data/CLIENTS.txt", header = TRUE, sep="\t", stringsAsFactors = TRUE)
  
  str(dataClients)
  summary(dataClients)
  apply(apply(dataClients,2, is.na),2,sum)
  nrow(dataClients[!complete.cases(dataClients),])
  
  # Corrigir Zone
  dataClients$Zone <- as.character(dataClients$Zone)
  dataClients$Zone[dataClients$Zone == "RIO TINTO - GONDOMAR"] <-  "GONDOMAR"
  dataClients$Zone <- as.factor(dataClients$Zone)
  dataClients$Zone <- droplevels(dataClients$Zone)
  
  # Vazios do MaritalStatus
  emptyPosition <- which(levels(dataClients$MaritalStatus) == "" )
  levels(dataClients$MaritalStatus)[emptyPosition] <- "NA"
  
  # Retirar Horas do timestamp
  dataClients$RegistrationDt <- as.Date(dataClients$RegistrationDt)
  dataClients$RegistrationDt <- format(dataClients$RegistrationDt, "%d-%m-%Y")
  
  # Ajustar City
  library(stringr)
  dataClients$City <- str_trim(dataClients$City)
  dataClients$City <- toupper(dataClients$City)
  
  unwanted_array = list('À'='A', 'Á'='A', 'Â'='A', 'Ã'='A', 'Ä'='A', 'Å'='A', 'Æ'='A', 'Ç'='A', 
                        'È'='E', 'É'='E', 'Ê'='E', 'Ë'='E', 'Ì'='A', 'Í'='I', 'Î'='O', 'Ï'='O', 
                        'Ò'='U', 'Ó'='O', 'Ô'='O', 'Õ'='O', 'Ö'='O', 'Ø'='O', 'Ù'='U', 'Ú'='U', 'Û'='U', 'Ü'='U')
  dataClients$City <- chartr(paste(names(unwanted_array), collapse=''), paste(unwanted_array, collapse=''), dataClients$City)
  
  dataClients$City[dataClients$City == "4425-536"] <-  "SAO PEDRO FINS"
  dataClients$City[dataClients$City == "MESAO-FRIO"] <-  "MESAO FRIO"
  
  # dataClients$City <- gsub("F", "E", dataClients$City)              NOT WORKING
  
  dataClients$City <- gsub("\u2039|\u2030", "A", dataClients$City)
  dataClients$City <- gsub("\u0090", "E", dataClients$City)
  dataClients$City <- gsub("\u008d", "C", dataClients$City)
  dataClients$City <- gsub("\u203a", "A", dataClients$City)
  
  dataClients$City <- gsub(",", "C", dataClients$City)
  dataClients$City <- gsub("'", "I", dataClients$City)
  
  
  dataClients$City <- gsub("(\\(.*\\))", "", dataClients$City) # retirar string entre ()
  dataClients$City <- gsub("\\s(\\(.*\\))", "", dataClients$City) # retirar string entre ()
  
  dataClients$City <- gsub("S\\. |S\\.", "SAO ", dataClients$City)
  dataClients$City <- gsub("ST|STA", "SANTA", dataClients$City)
  dataClients$City <- gsub("STO", "SANTO", dataClients$City)
  
  dataClients$City <- gsub("ESP\\.", "ESPADA", dataClients$City)
  
  dataClients$City <- gsub("V\\. N\\. |V\\. N\\.|V\\.N\\.", "VILA NOVA DE ", dataClients$City)
  
  # Retirar siglas de cidades
  dataClients$City[dataClients$City == "LORDELO-PAREDES"] <-  "LORDELO"
  dataClients$City[dataClients$City == "MADALENA - PICO"] <-  "MADALENA"
  dataClients$City[dataClients$City == "PEDROSO-CARVALHOS"] <-  "PEDROSO"
  dataClients$City[dataClients$City == "VALBOM-GDM"] <-  "VALBOM"
  dataClients$City[dataClients$City == "CUSANTAOIAS-MTS"] <-  "CUSANTAOIAS"
  
  dataClients$City <-  gsub(" AMT| VNT| VLP| TRF| EPS| VNG| MCN| VFR| TMR| GMR| VNB| BRG| LSD| VCD| BCL
                            | AMR| AFD| RSD| PRD| PNF| ALB| VVD| MTR| VLG| VNC| PDL| VFR| BCL| MDL| BBR
                            | VNF| TND| OVR| VRL| PCR| GMD| MTS| AGD| GDM| BBR| CNF| PVL| CBT| PTL| FLG
                            | VIZ| HRT| LRS| LRA| BGC| MMV| SMP| ARC| TVD| ETR| TBR| BAO| CMN| SVV| MDA
                            | AVV| FLG| VDG| PTB| MDA", "", dataClients$City)
  
  dataClients$City <- as.factor(dataClients$City)
  dataClients$City <- droplevels(dataClients$City)
  # sort(unique(dataClients$City))
  
  
  
  # ------------------------------ Clients Pre Processamento -----------------------------------------
  
  GroupAge <- cut(dataClients$Age, breaks= c(0, 30, 50, +Inf), labels= c("Young", "Middle Aged", "Elderly"), right=FALSE, ordered_result=TRUE)
  table(GroupAge)
  dataClients <- cbind(dataClients, GroupAge)
  
  
  
  # ------------------------------ Purchases Limpeza de Dados -----------------------------------------
  
  dataPuchases <- read.table(file="C:/Users/ricar/Desktop/DESCO/desco/Trabalho Parte 1/Data/PURCHASES.txt", 
                             header = TRUE, sep="\t", stringsAsFactors = TRUE)
  #
  str(dataPuchases)
  summary(dataPuchases)
  apply(apply(dataPuchases,2, is.na),2,sum) 
  nrow(dataPuchases[!complete.cases(dataPuchases),])
  
  # Verificar e tratar de strings vazias para NA
  for (i in 1: ncol(dataPuchases)) {
    emptyPosition <- which(levels(dataPuchases[,i]) == "" )
    levels(dataPuchases[i])[emptyPosition] <- "NA"
  }
  
  # Remover * do inï¿½cio das descriï¿½ï¿½es
  dataPuchases$DESCR<- as.character(dataPuchases$DESCR)
  for(i in 1: nrow(dataPuchases)) {
    if(substring(dataPuchases$DESCR[i],1,1)=="*") {
      dataPuchases$DESCR[i]<-substring(dataPuchases$DESCR[i], 2)
    }
    # print(dataPuchases$DESCR[i])
  }
  dataPuchases$DESCR<- as.factor(dataPuchases$DESCR)
  
  # Corrigir TAX
  library(stringr)
  dataPuchases$TAX <- str_trim(dataPuchases$TAX)
  dataPuchases$TAX <- toupper(dataPuchases$TAX)
  dataPuchases$TAX <- as.factor(dataPuchases$TAX)
  dataPuchases$TAX <- droplevels(dataPuchases$TAX)
  
  
  
  
  # ------------------------------ Purchases Pre Processamento -----------------------------------------
  
  # ANALIZAR VALORES NUMERICOS
  library(e1071)
  ?skewness()
  numericAttrs <- dataPuchases[,sapply(dataPuchases,is.numeric)]
  numericAttrNames <- colnames(numericAttrs)
  skewness <- apply(dataPuchases[,numericAttrNames], 2, skewness) # assimetria
  sort(skewness, decreasing = TRUE)
  summary(numericAttrs) # ver o range de valores numericos
  
  library(corrplot)
  correlationMatrix <- cor(numericAttrs) # correlacao entre todos os atributos nao objetivos da tabela
  colsToRemove <- c("PACKAGE", "PACKAGEFACT") # PACKAGE e PACKAGEFACT nao variam
  dataPuchases <- dataPuchases[, !names(dataPuchases) %in% colsToRemove]
  
  # Analisar Departament Attr
  table(dataPuchases$DEPARTMENT) # muito mais distrubidas as classes
  dataPuchases[dataPuchases$DEPARTMENT == "Estetica", ] # Apenas maquilhagem e manicure
  dataPuchases[dataPuchases$DEPARTMENT == "NO DEPARTMENT", ] # Mairiotirariamente Cremes e Mascaras
  # Ambos fazem sentido serem adicionados ao departamento de cosmetica
  dataPuchases$DEPARTMENT[dataPuchases$DEPARTMENT == "Estetica"] <- "Cosmetica"
  dataPuchases$DEPARTMENT[dataPuchases$DEPARTMENT == "NO DEPARTMENT"] <- "Cosmetica"
  dataPuchases$DEPARTMENT <- droplevels(dataPuchases$DEPARTMENT)
  
  
  
  # ------------------------------ Merged -----------------------------------------
  
  # Merge dataClients e dataPuchases
  dataMerged <- merge(dataClients, dataPuchases, by.x="Client", by.y="ENTITY")
  dataMerged
  correlationMatrix <- cor(dataMerged) # correlacao entre todos os atributos nao objetivos da tabela
  
  
  
  # ------------------------------ Graficos Clients  ------------------------------
  
  library(RColorBrewer)
  coul <- brewer.pal(8, "Set1") 
  
  
  # Grï¿½fico de comparaï¿½ï¿½o de gï¿½neros dos clientes
  barplot(table(dataClients$Gender), ylim=c(0,10000), main="Nï¿½mero de clientes por gï¿½nero",col=c("pink","lightblue"),names.arg=c("Feminino","Masculino"))
  
  
  # GrÃ¡fico de comparaÃ§Ã£o de Idades dos clientes
  barplot(table(dataClients$GroupAge), main="Idade dos Clientes",col=coul,horiz=T,xlim =c(0,8000))
  
  
  # Clientes -> Idades Vs Genero
  boxplot(dataClients$Age ~ dataClients$Gender, col=c("pink","lightblue"), main="Distribuição Idade por Género",  xlab="Gender", ylab="Age")
  
  barplot(table(dataClients$Gender, dataClients$GroupAge), beside = T, col=c(2,5), ylim=c(0,5000), main="Distribuiï¿½ï¿½o Idade por Gï¿½nero")
  legend(list(x = 1.25,y = 4500), levels(dataClients$Gender), fill=c(2,5))
  
  
  #  Clientes -> Zone vs (Idades Vs Genero)
  par(mfrow=c(2,2)) # matriz 2 por 2 para apresentar graficos
  
  for (zone in sort(unique(dataClients$Zone))) {
    rowsForZone <- dataClients[dataClients$Zone == zone, ]
    boxplot(rowsForZone$Age ~ rowsForZone$Gender, col=c(2,5), main=zone, xlab="Gender", ylab="Age")
  }
  mtext(expression(paste(bold("Distribuição Idade por Gï¿½nero por Zona"))), side = 3, line = -17.3, outer = TRUE)
  
  
  # Clientes -> Zone vs (Idades Vs Genero)
  par(mfrow=c(2,2)) # matriz 2 por 2 para apresentar graficos
  
  for (zone in sort(unique(dataClients$Zone))) {
    rowsForZone <- dataClients[dataClients$Zone == zone, ]
    barplot(table(rowsForZone$Gender, rowsForZone$GroupAge), beside = T, col=c(2,5), ylim=c(0,3000), main=zone)
  }
  mtext(expression(paste(bold("Distribuição Idade por Género por Zona"))), side = 3, line = -17, outer = TRUE)
  
  
  # Percentagem de Filhos por Cliente
  par(mfrow=c(1,1))
  
  slices <- table(dataClients$NumChildren)
  lbls <- rownames(slices)
  lbls <- paste(lbls, "Filhos (")
  pct <- round(slices / sum(slices) * 100)
  lbls <- paste(lbls, pct, sep = "")
  lbls <- paste(lbls, "%)", sep = "")
  
  pie(slices, labels = lbls, col = coul, main = "Percentagem de Filhos por Cliente")
  
  
  
  
  # -------------- Graficos Purchases ---------------------
  
  #Nï¿½mero de vendas por ano
  library(plyr)
  purchasesByYear <- count(dataPuchases,"YEAR")
  barplot(as.matrix(purchasesByYear)[,2], main = "Número de vendas por ano",col=coul,ylim=c(0,130000), names.arg=c("2011","2012","2013","2014"))
  
  library(lubridate)
  par(mfrow=c(2,2))
  #2011
  AKA <-ymd_hms(dataPuchases$DATE[dataPuchases$YEAR=="2011"])
  ae <-quarter(AKA, 
               with_year = FALSE)
  barplot(table(ae),
          col=coul,
          ylim=c(0,4000),
          names.arg=c("4th Tri"), 
          main="2011")
  
  #2012
  AKA <-ymd_hms(dataPuchases$DATE[dataPuchases$YEAR=="2012"])
  ae <-quarter(AKA, 
               with_year = FALSE)
  barplot(table(ae),
          col=coul,
          ylim=c(0,80000),
          names.arg=c("1st Tri","2nd Tri","3rdTri","4th Tri"), 
          main="2012")
  #2013
  AKA <-ymd_hms(dataPuchases$DATE[dataPuchases$YEAR=="2013"])
  ae <-quarter(AKA, 
               with_year = FALSE)
  barplot(table(ae),
          col=coul,
          ylim=c(0,80000),
          names.arg=c("1st Tri","2nd Tri","3rdTri","4th Tri"), 
          main="2013")
  #2014
  AKA <-ymd_hms(dataPuchases$DATE[dataPuchases$YEAR=="2014"])
  ae <-quarter(AKA, 
               with_year = FALSE)
  barplot(table(ae),
          col=coul,
          ylim=c(0,80000),
          names.arg=c("1st Tri","2nd Tri","3rd Tri"),
          main="2014")
  # APENAS Hï¿½ DADOS DO ULTIMO SEMESTRE DE 2011 E DOS 3 PRIMEIROS DE 2014, MOTIVO PELO QUAL Nï¿½O EXISTE GRï¿½FICO PARA 2011
  mtext(expression(paste(bold("Numero de vendas por ano"))),
        side = 3,
        line = -19, 
        outer = TRUE)
  
  
  # DEPARTMENT VS CODDOC
  par(mfrow=c(1,1))
  library(RColorBrewer)
  coul <- brewer.pal(4, "Set1") 
  addmargins(table(dataPuchases$DEPARTMENT, dataPuchases$CODDOC)) # add Sum col and row
  barplot(table(dataPuchases$DEPARTMENT, dataPuchases$CODDOC), beside = T, col=coul, ylim = c(0,150000), main= "DEPARTMENT VS CODDOC")
  legend("topright", levels(dataPuchases$DEPARTMENT), fill=coul)
  
  
  # Percentagem de Vendas por Departamento
  slices <- table(dataPuchases$DEPARTMENT)
  lbls <- rownames(slices)
  lbls <- paste(lbls, "(")
  pct <- round(slices / sum(slices) * 100)
  lbls <- paste(lbls, pct, sep = "")
  lbls <- paste(lbls, "%)", sep = "")
  pie(slices, labels = lbls, col = coul, main = "Percentagem Vendas por Departamento")
  
  
  # Compras em cada departamento do ano
  coul2 <- brewer.pal(4, "Set1") 
  barplot(table(dataPuchases$YEAR,dataPuchases$DEPARTMENT), main = "Compras em cada departamento por ano", ylab = "Compras", xlab = "Departamento", col = coul2, beside = TRUE)
  legend("topleft",legend = c("2011","2012","2013","2014"), col = coul2, 
         bty = "n", pch=20 , pt.cex = 2, cex = 0.8, horiz = FALSE, inset = c(0.05, 0.05))
  
  
  # Numero de Produtos diferentes por Departamento por Suplier
  table(dataPuchases$PRODUCT, dataPuchases$DEPARTMENT)
  productsForSupForDep <- aggregate(dataPuchases["PRODUCT"], by=list(dataPuchases$DEPARTMENT, dataPuchases$SUPLIER), FUN=length)
  productsForSupForDep
  
  
  
  # -------------- Graficos Merged ---------------------
  
  # Vendas por idade de cliente por Product type
  productsForTypeForAge <- aggregate(dataMerged["PRODUCT"], by=list(dataMerged$PRODUCTYPE, dataMerged$GroupAge), FUN=length)
  productsForTypeForAge
  
  # Vendas por idade de cliente por Departamento
  
  
  productsForDepForAge <- aggregate(dataMerged["PRODUCT"], by=list(dataMerged$DEPARTMENT, dataMerged$GroupAge), FUN=length)
  productsForDepForAge
  barplot(table(dataMerged$DEPARTMENT, dataMerged$GroupAge), beside = T, col=coul, ylim = c(0,160000), main= "DEPARTMENT VS AGE")
  legend(list(x = 1.25,y = 150000), levels(dataMerged$DEPARTMENT), fill=coul)
  
  
  
  # ------------------------------ RFM Analisys -----------------------------------------
  # Recency - How recently customer purchased
  # Frequency - How Frequently customer purchased
  # Montary - How much money customer spent
  # https://www.r-bloggers.com/2019/07/customer-segmentation-using-rfm-analysis/
  
  library(rfm)
  
  rfmDataAggregate <- aggregate(dataMerged["TOTAL"], by=list(dataMerged$Client, dataMerged$DATE), FUN=sum)
  rfmData <- data.frame(customer_id = rfmDataAggregate$Group.1, order_date = rfmDataAggregate$Group.2, revenue = rfmDataAggregate$TOTAL)
  rfmData$order_date <- as.Date(rfmData$order_date)
  rfmData$revenue <- as.numeric(rfmData$revenue)
  analysis_date <-  lubridate::as_date(max(rfmData$order_date), tz= "UTC")
  
  rfmResult <- rfm_table_order(rfmData, customer_id, order_date, revenue, analysis_date)
  
  
  
  # -------------------------- Analisar RFM --------------------------------------------
 x
   library(rfm)
  rfm_heatmap(rfmResult)
  rfm_histograms(rfmResult)
  rfm_rm_plot(rfmResult)
  rfm_fm_plot(rfmResult)
  rfm_rf_plot(rfmResult)
  # -------------------------- Clustering ---------------------------------------------
  
  library(cluster)
  
  # fazer clustering com os dados do RFM e dados demograficos do cliente
  rfmResultTibble <- rfmResult$rfm
  rfmResultDataFrame <- as.data.frame(rfmResultTibble)
  dataClustering <- merge(dataClients, rfmResultDataFrame, by.x="Client", by.y="customer_id")
  
  # Retirar RegistrationDt, MaritalStatus, HasChildren, PostalCode, GroupAge, 
  # date_most_recent, recency_score, frequency_score, monetary_score, rfm_score
  dataClustering<-dataClustering[,-c(2,5,6,8,11,12,16,17,18,19)]
  dataClustering$Gender <- as.integer(dataClustering$Gender)
  dataClustering$Zone <- as.integer(dataClustering$Zone)
  dataClustering$City <- as.integer(dataClustering$City)
  
  
  # Normalize as variáveis numéricas, usando a função scale()
  dataClustering.std <- scale(dataClustering[,-1])
  summary(dataClustering.std)
  
  # centro normalizacao
  pcenter <- attr(dataClustering.std, "scaled:center") # centro colunas
  pscale <- attr(dataClustering.std, "scaled:scale") # desvio padrao colunas
  class(dataClustering.std)
  
  # passar para dataframe
  dataClustering.std <- data.frame(scale(dataClustering[,-1]))
  
  # Execute o algoritmo K-means, com K = 3 e com múltiplas iterações e inicializações aleatórias do
  # algoritmo, de modo a melhorar a estabilidade do resultado.
  dataClustering.k3 <- kmeans(dataClustering.std, centers=3, iter.max=100, nstart = 25)
  plot(dataClustering.k3)
  
  install.packages(("factoextra"))
  library(factoextra) # clustering algorithms & visualization
  fviz_cluster(dataClustering.k3, data = dataClustering.std)
  
  # 1 d. Avalie a segmentação obtida usando o coeficiente de silhouette.
  dist <- dist(dataClustering.std)
  sil <- silhouette(dataClustering.k3$cluster, dist)
  summary(sil)
  plot(sil)
  # coeficiente de silhouette quanto mais proximo de 1, melhor  o clustering
  # melhor é  k=3
  
  # Encontre a melhor partição para este conjunto de dados usando o coeficiente de silhouette.
  # DEMORA MUITO
  #library(fpc)
  #kclusters <- kmeansruns(dataClustering.std, frange=2:10, criterion="asw")
  
  #kclusters$crit # varios coeficiente de silhouette para cada k
  #kclusters$bestk
  
  #plot(c(1:10), kclusters$crit, type="b", xlab="N. clusters", ylab="Avg. Silhouette")
  
  # Caracterize os clusters encontrados
  par(mfrow=c(1,3))
  
  plot(dataClustering.std[, c("recency_days", "transaction_count")], col=dataClustering.k3$cluster)
  points(dataClustering.k3$center[, c("recency_days", "transaction_count")], col=1:3, pch=8, cex=2)
  legend("bottomright", pch=1, col=1:3, legend=c("1", "2", "3"))
  
  plot(dataClustering.std[, c("recency_days", "amount")], col=dataClustering.k3$cluster)
  points(dataClustering.k3$center[, c("recency_days", "amount")], col=1:3, pch=8, cex=2)
  legend("bottomright", pch=1, col=1:3, legend=c("1", "2", "3"))
  
  plot(dataClustering.std[, c("transaction_count", "amount")], col=dataClustering.k3$cluster)
  points(dataClustering.k3$center[, c("transaction_count", "amount")], col=1:3, pch=8, cex=2)
  legend("bottomright", pch=1, col=1:3, legend=c("1", "2", "3"))
  
  # Diferencas por cluster
  library(RColorBrewer)
  coul <- brewer.pal(8, "Set3") 
  par(mfrow=c(1,1))
  dataClustering.k3$center # coordenadas do centro
  barplot(t(dataClustering.k3$center), beside=TRUE, xlab="cluster", ylab="value", col=coul, ylim = c(-2,2.5))
  legend("topleft",  fill=coul, legend=c("Age", "Gender", "NumChildren", "Zone", "City", "recency_days", "transaction_count", "amount"))
  
  plot(dataClustering.k3)
  
  # Separar clusters por dataframes
  
  dataMerged <- dataMerged[,-c(2,5,6,8,13,14,15,16,23,24,25,26,27,28)]
  
  ClientByCluster = split(dataClustering, dataClustering.k3$cluster)
  
  dataMergedForCluster1 <- data.frame()
  dataMergedForCluster2 <- data.frame();
  dataMergedForCluster3 <- data.frame();
  dataClientForCluster1 <- data.frame()
  dataClientForCluster2 <- data.frame();
  dataClientForCluster3 <- data.frame();
  
  for (i in c(1:length(dataClustering.k3$cluster))) {
    
    if (dataClustering.k3$cluster[i] == 1) {
      dataMergedForCluster1  <- rbind(dataMergedForCluster1, dataMerged[dataMerged[, "Client"] == dataClustering$Client[i],])
      dataClientForCluster1 <- rbind(dataClientForCluster1,dataClients[dataClients[,"Client"]==dataClustering$Client[i],])
    } else if(dataClustering.k3$cluster[i] == 2) {
      dataMergedForCluster2  <- rbind(dataMergedForCluster2, dataMerged[dataMerged[, "Client"] == dataClustering$Client[i],])
      dataClientForCluster2 <- rbind(dataClientForCluster2,dataClients[dataClients[,"Client"]==dataClustering$Client[i],])
    } else if(dataClustering.k3$cluster[i] == 3) {
      dataMergedForCluster3  <- rbind(dataMergedForCluster3, dataMerged[dataMerged[, "Client"] == dataClustering$Client[i],])
      dataClientForCluster3 <- rbind(dataClientForCluster3,dataClients[dataClients[,"Client"]==dataClustering$Client[i],])
    }
  }
  
  
  
  # ------------------------- Cluster Analysis ---------------------------------------
  
  # https://rstudio-pubs-static.s3.amazonaws.com/33876_1d7794d9a86647ca90c4f182df93f0e8.html
  attach(mtcars)
  par(mfrow=c(2,2))
  barplot(table(dataClientForCluster1$Gender), ylim=c(0,3500), main="Cluster 1",col=c("pink","lightblue"),names.arg=c("Feminino","Masculino"))
  barplot(table(dataClientForCluster2$Gender), ylim=c(0,3500), main="Cluster 2",col=c("pink","lightblue"),names.arg=c("Feminino","Masculino"))
  barplot(table(dataClientForCluster3$Gender), ylim=c(0,3500), main="Cluster 3",col=c("pink","lightblue"),names.arg=c("Feminino","Masculino"))
  mtext(expression(paste(bold("Género dos Clientes"))), side = 3, line = -15.3, outer = TRUE)
  
  par(mfrow=c(2,2))
  # GrÃ¡fico de comparaÃ§Ã£o de Idades dos clientes
  barplot(table(dataClientForCluster1$GroupAge), main="Cluster 1",col=coul,horiz=T,xlim =c(0,4000))
  barplot(table(dataClientForCluster2$GroupAge), main="Cluster 2",col=coul,horiz=T,xlim =c(0,4000))
  barplot(table(dataClientForCluster3$GroupAge), main="Cluster 3",col=coul,horiz=T,xlim =c(0,4000))
  mtext(expression(paste(bold("Idade dos Clientes"))), side = 3, line = -28.3, outer = TRUE)
  
  # Clientes -> Idades Vs Genero
  
  par(mfrow=c(2,2)) 
  boxplot(dataClientForCluster1$Age ~ dataClientForCluster1$Gender, col=c("pink","lightblue"), main="Cluster 1",  xlab="Gender", ylab="Age")
  boxplot(dataClientForCluster2$Age ~ dataClientForCluster2$Gender, col=c("pink","lightblue"), main="Cluster 2",  xlab="Gender", ylab="Age")
  boxplot(dataClientForCluster3$Age ~ dataClientForCluster3$Gender, col=c("pink","lightblue"), main="Cluster 3",  xlab="Gender", ylab="Age")
  mtext(expression(paste(bold("Idade por Genero"))), side = 3, line = -28.3, outer = TRUE)
  
  #  Clientes -> Zone vs (Idades Vs Genero)
  par(mfrow=c(2,2)) # matriz 2 por 2 para apresentar graficos
  
  for (zone in sort(unique(dataClientForCluster1$Zone))) {
    rowsForZone <- dataClientForCluster1[dataClientForCluster1$Zone == zone, ]
    # boxplot(rowsForZone$Age ~ rowsForZone$Gender, col=c(2,5), main=zone, xlab="Gender", ylab="Age")
    barplot(table(rowsForZone$Gender), ylim=c(0,1200), main=zone,col=c("pink","lightblue"),names.arg=c("Feminino","Masculino"))
  }
  mtext(expression(paste(bold("Cluster 1"))), side = 3, line = -18.0, outer = TRUE)

  par(mfrow=c(2,2)) # matriz 2 por 2 para apresentar graficos
  for (zone in sort(unique(dataClientForCluster2$Zone))) {
    rowsForZone <- dataClientForCluster2[dataClientForCluster2$Zone == zone, ]
    # boxplot(rowsForZone$Age ~ rowsForZone$Gender, col=c(2,5), main=zone, xlab="Gender", ylab="Age")
    barplot(table(rowsForZone$Gender), ylim=c(0,800), main=zone,col=c("pink","lightblue"),names.arg=c("Feminino","Masculino"))
    
  }
  mtext(expression(paste(bold("Cluster 2"))), side = 3, line = -18.0, outer = TRUE)
  
  par(mfrow=c(2,2)) # matriz 2 por 2 para apresentar graficos
  for (zone in sort(unique(dataClientForCluster3$Zone))) {
    rowsForZone <- dataClientForCluster3[dataClientForCluster3$Zone == zone, ]
    # boxplot(rowsForZone$Age ~ rowsForZone$Gender, col=c(2,5), main=zone, xlab="Gender", ylab="Age")
    barplot(table(rowsForZone$Gender), ylim=c(0,3500), main=zone,col=c("pink","lightblue"),names.arg=c("Feminino","Masculino"))
  }
  mtext(expression(paste(bold("Cluster 3"))), side = 3, line = -18.0, outer = TRUE)
  

  
  # Percentagem de Filhos por Cliente
  par(mfrow=c(1,1))
  
  slices <- table(dataClientForCluster1$NumChildren)
  lbls <- rownames(slices)
  lbls <- paste(lbls, "Filhos (")
  pct <- round(slices / sum(slices) * 100)
  lbls <- paste(lbls, pct, sep = "")
  lbls <- paste(lbls, "%)", sep = "")
  
  pie(slices, labels = lbls, col = coul, main = "Percentagem de Filhos por Cliente Cluster 1")
  

  
  slices <- table(dataClientForCluster2$NumChildren)
  lbls <- rownames(slices)
  lbls <- paste(lbls, "Filhos (")
  pct <- round(slices / sum(slices) * 100)
  lbls <- paste(lbls, pct, sep = "")
  lbls <- paste(lbls, "%)", sep = "")
  
  pie(slices, labels = lbls, col = coul, main = "Percentagem de Filhos por Cliente Cluster 2")

  
  slices <- table(dataClientForCluster3$NumChildren)
  lbls <- rownames(slices)
  lbls <- paste(lbls, "Filhos (")
  pct <- round(slices / sum(slices) * 100)
  lbls <- paste(lbls, pct, sep = "")
  lbls <- paste(lbls, "%)", sep = "")
  
  pie(slices, labels = lbls, col = coul, main = "Percentagem de Filhos por Cliente Cluster 3")
  
  
  # -------------------------- Regras de Associacao ------------------------------------
  
  library("lubridate")
  library("plyr")
  library(arules)
  
  # --- Cluster 1
  
  # Com os dados anteriormente carregados crie um objecto basket
  basket <- as(split(as.vector(dataMergedForCluster1$PRODUCTYPE), as.vector(dataMergedForCluster1$Client)), "transactions")
  inspect(basket[1:5])
  
  # Visualize a frequência dos itens numericamente
  itemFreq <- itemFrequency(basket)
  itemFreq
  itemFrequency(basket[,1:3])
  # Contabilize o nº de cestos em que cada item aparece
  itemCount <- (itemFreq / sum(itemFreq))*sum(size(basket))
  itemCount
  
  # Aplique o algoritmo Apriori para extração de Regras de Associação com Supmin=5% e Confmin = 80%
  basketRules <- apriori(basket, parameter = list(support=0.05, confidence=0.80, minlen=2))
  summary(basketRules)
  
  # Para o conjunto de regras anteriormente gerado visualize:
  
  # i. a gama de valores das medidas Coverage, Conviction e Leverage
  measures <- interestMeasure(basketRules, 
                              measure = c("coverage", "leverage", "conviction"), 
                              transactions = basket)
  measures
  
  # ii. as  regras
  inspect(basketRules)
  inspect(basketRules[1:10])
  # iii. as 15 regras com maior lift
  inspect(sort(basketRules, by="lift")[1:15])
  
  # iii. Confiança × Suporte (Nº itens da regra)
  plot(basketRules, shading="order", control=list(main="Two-key plot"), jitter=0)
 
  itemFrequencyPlot(basket, topN = 20, 
                            col = brewer.pal(8, 'Pastel2'),
                            main = 'Relative Item Frequency Plot',
                            type = "relative",
                            ylab = "Item Frequency (Relative)")
  
  # --- Cluster 2
  # Com os dados anteriormente carregados crie um objecto basket
  basket <- as(split(as.vector(dataMergedForCluster2$PRODUCTYPE), as.vector(dataMergedForCluster2$Client)), "transactions")
  inspect(basket[1:5])
  
  # Visualize a frequência dos itens numericamente
  itemFreq <- itemFrequency(basket)
  itemFreq
  itemFrequency(basket[,1:3])
  # Contabilize o nº de cestos em que cada item aparece
  itemCount <- (itemFreq / sum(itemFreq))*sum(size(basket))
  itemCount
  
  # Aplique o algoritmo Apriori para extração de Regras de Associação com Supmin=5% e Confmin = 80%
  basketRules <- apriori(basket, parameter = list(support=0.05, confidence=0.80, minlen=2))
  summary(basketRules)
  
  # Para o conjunto de regras anteriormente gerado visualize:
  
  # i. a gama de valores das medidas Coverage, Conviction e Leverage
  measures <- interestMeasure(basketRules, 
                              measure = c("coverage", "leverage", "conviction"), 
                              transactions = basket)
  measures
  
  # ii. as  regras
  inspect(basketRules)
  inspect(basketRules[1:15])
  # iii. as 15 regras com maior lift
  inspect(sort(basketRules, by="lift")[1:15])
  
  # iii. Confiança × Suporte (Nº itens da regra)
  plot(basketRules, shading="order", control=list(main="Two-key plot"), jitter=0)
  
  itemFrequencyPlot(basket, topN = 20, 
                    col = brewer.pal(8, 'Pastel2'),
                    main = 'Relative Item Frequency Plot',
                    type = "relative",
                    ylab = "Item Frequency (Relative)")
  # --- Cluster 3
  # Com os dados anteriormente carregados crie um objecto basket
  basket <- as(split(as.vector(dataMergedForCluster3$PRODUCTYPE), as.vector(dataMergedForCluster3$Client)), "transactions")
  inspect(basket[1:5])
  
  # Visualize a frequência dos itens numericamente
  itemFreq <- itemFrequency(basket)
  itemFreq
  itemFrequency(basket[,1:3])
  # Contabilize o nº de cestos em que cada item aparece
  itemCount <- (itemFreq / sum(itemFreq))*sum(size(basket))
  itemCount
  
  # Aplique o algoritmo Apriori para extração de Regras de Associação com Supmin=5% e Confmin = 80%
  basketRules <- apriori(basket, parameter = list(support=0.05, confidence=0.80, minlen=2))
  summary(basketRules)
  
  # Para o conjunto de regras anteriormente gerado visualize:
  
  # i. a gama de valores das medidas Coverage, Conviction e Leverage
  measures <- interestMeasure(basketRules, 
                              measure = c("coverage", "leverage", "conviction"), 
                              transactions = basket)
  measures
  
  # ii. as  regras
  inspect(basketRules)
  inspect(basketRules[1:15])
  # iii. as 15 regras com maior lift
  inspect(sort(basketRules, by="lift")[1:15])
  
  #install.packages("arulesViz")
  library(arulesViz)
  # iii. Confiança × Suporte (Nº itens da regra)
  plot(basketRules, shading="order", control=list(main="Two-key plot"), jitter=0)
  itemFrequencyPlot(basket, topN = 20, 
                    col = brewer.pal(8, 'Pastel2'),
                    main = 'Relative Item Frequency Plot',
                    type = "relative",
                    ylab = "Item Frequency (Relative)")
  
  
  
  # -------------------------- Modelos de Classificacao ---------------------------------
  results <- data.frame(model = character(), accuracy = double(), kappa = double(),
                        recall = double(), precision = double(), f1 = double(), stringsAsFactors = FALSE)
  library(caret)
  library(class)
  library(gmodels)
  allcrosstablemeasures <- function (test_labels, prediction, modelname="") {
   
      
      crosstb <- CrossTable(test_labels, prediction,
                            prop.chisq = FALSE, prop.c = FALSE,
                            prop.r = FALSE, dnn = c("Actual", "Predicted"))
      
      accuracy <- sum(diag(crosstb$t))/sum(crosstb$t) # accuracy(Tx. acerto)

      
      cm <-confusionMatrix(crosstb[[1]])
      print(cm[["byClass"]][ , "Precision"]) #for multiclass classification problems
      print(cm[["byClass"]][ , "Recall"]) #for multiclass classification problems
 
     # recall <- crosstb[[1]][1,1]/sum(crosstb[[1]][1,]) # TPR(Recall)
      #precision <- crosstb[[1]][1,1]/sum(crosstb[[1]][,1]) #Precision
      #fpr <- crosstb[[1]][2,1]/sum(crosstb[[1]][2,]) 
      #f1 <- 2*precision*recall/(precision+recall) # F1 measuere
      
      #randAcc <- sum(crosstb[[1]][1,]) *sum(crosstb[[1]][,1]) + sum(crosstb[[1]][2,]) * sum(crosstb[[1]][,2])
      #randAcc <- randAcc/(sum(crosstb$t)*sum(crosstb$t))
      
    #  kappa <- (accuracy-randAcc)/(1-randAcc)
      
     data.frame(model = modelname, accuracy = round(accuracy,digits=3))# precision=precision[1])
     #, kappa = round(kappa,digits=3),
      #           recall = round(recall,digits=3), precision = round(precision,digits=3), f1 = round(f1,digits=3))
    
  }
  # Neural net --------------------------------------------

  set.seed(123)
  fullClassData<-dataClustering.std[,-(5:8),drop=FALSE]
  fullClassData$Cluster <-factor(dataClustering.k3$cluster)
#install.packages("caret")
  library(caret)
  trainIndex <- createDataPartition(fullClassData$Cluster, p=0.7, list=F)
  train <- fullClassData[trainIndex, ]
  test <- fullClassData[-trainIndex, ]
  
 # install.packages(("nnet"))
  library(nnet)
  
  
  fishing1<-nnet(Cluster~.,data=train,size=15, maxit=1500)


 k<- predict(fishing1, test[-5],type = "class")

  x <-data.frame(Actual = test$Cluster, Predicted=k)
  abcd <- confusionMatrix(test$Cluster, as.factor(k))
  abcd
  results <- rbind(results, allcrosstablemeasures(test$Cluster, as.factor(k), modelname = "ANN"))
  results
  
  
  # C5.0 -------------------------------------------

  #install.packages("C50")
  
  library(C50)
  
  C5Model <- C5.0(train[-5], train$Cluster)
  summary(C5Model)
  plot(C5Model)
  C5pred <- predict(C5Model, test[-5])
  
  results <- rbind(results, allcrosstablemeasures(test$Cluster, C5pred, modelname = "C50"))
  results
 
  
  
  #knn ---------------------------------------------
  
#  install.packages("class")
 # install.packages("gmodels")
  
  k <- c()
  falsosPositivos <- c()
  falsosNegativos <- c()
  accuracy <- c()
 
    predictions <- knn(train[-5] , test[-5] , cl = train$Cluster, k = 3)

  results <- rbind(results, allcrosstablemeasures(test$Cluster, predictions, modelname = "KNN"))
  results
  
  # NAIVE BAYES

 # install.packages("e1071")
  library(class)
  library(gmodels)
  library(e1071)
  set.seed(123)
  bayesModel <- naiveBayes(Cluster~., data = train, laplace = 1)
  NBpredict <- predict(bayesModel, newdata = test[-5], type="class")
  results <- rbind(results, allcrosstablemeasures(test$Cluster, NBpredict, modelname = "Naive Bayes"))
  results

  
  # Random Forests ------------------
  
  #install.packages(("randomForest"))
  library(randomForest)
  rf <- randomForest(
  Cluster ~ ., data=train
  )

  pred = predict(rf, newdata=test[-5])
  results <- rbind(results, allcrosstablemeasures(test$Cluster, pred, modelname = "Random Forests"))
  results
  
  
  
  #install.packages("kernlab")
  #  Support Vector Machines (SVM) kernel: tanhdot
  library(kernlab)
  set.seed(123)
  SVNmodel <- ksvm(Cluster ~., data = train, kernel = "tanhdot", C=1, prob.model = TRUE)
  SVNmodel
  SVNpredict <- predict(SVNmodel, newdata = test[-5])
  results <- rbind(results, allcrosstablemeasures(test$Cluster, SVNpredict, modelname = "Support Vector Machines (kernel: tanhdo)"))
  
  #  Support Vector Machines (SVM) kernel: vanilladot
  library(kernlab)
  set.seed(123)
  SVNmodel <- ksvm(Cluster ~., data = train, kernel = "vanilladot", C=1, prob.model = TRUE)
  SVNmodel
  SVNpredict <- predict(SVNmodel, newdata = test[-5])
  results <- rbind(results, allcrosstablemeasures(test$Cluster, SVNpredict, modelname = "Support Vector Machines (kernel: vanilladot)"))
  
  #  Support Vector Machines (SVM) kernel: rbfdot
  library(kernlab)

  SVNmodel <- ksvm(Cluster~., data = train, kernel = "rbfdot", C=1, prob.model = TRUE)
  SVNmodel
  SVNpredict <- predict(SVNmodel, newdata = test[-5])
  results <- rbind(results, allcrosstablemeasures(test$Cluster, SVNpredict, modelname = "Support Vector Machines (kernel: rbfdot)"))
  
  results
  