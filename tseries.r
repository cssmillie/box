read_tseries = function(fn, std=TRUE){
    require(data.table)
    # Read time series as zoo object
    x = fread(fn, sep='\t', header=TRUE)
    x = data.frame(x[,-1,with=FALSE], row.names=x[[1]])
    as.matrix(x)
    # Fix zeros @ .5*min
    x = fix_zeros(x, method='min')
    # Standardize if necessary
    if(std == TRUE){
        x = scale(x)
    }
    # Return zoo object
    return(x)
}

fit_arima = function(x){
    require(forecast)
    # Fit ARIMA model to each column of x
    y = as.data.frame(apply(x, 2, function(a) fitted(auto.arima(a))[-1]))
    z = list(fitted = y, residuals = x[1:(nrow(x)-1),]-y)
    return(z)
}

fix_zeros = function(x, method='min'){
    if(method == 'min'){
        x = as.matrix(x)
        x[x < -20] = log(.5) + min(x[x > -20])
        x = as.data.frame(x)
    }
    return(x)
}