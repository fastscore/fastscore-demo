# fastscore.schema.0: double
# fastscore.schema.1: double

action <- function(datum){
  # hello, world!
    emit(datum + 1)
}
