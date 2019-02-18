# fastscore.slot.0: in-use
# fastscore.slot.1: in-use
# fastscore.module-attached: gbm
library(tidyverse)
library(padr)
library(zoo)
library(forecast)
library(lubridate)
library(jsonlite)


# Sample input: {"x":5.0, "y":6.0}
action <- function(datum) {
  x <- datum$x
  y <- datum$y
  emit(x + y)
}
