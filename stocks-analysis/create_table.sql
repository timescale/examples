/* Creates the table which will store stock data */
CREATE TABLE public.stocks2 (
	stock_datetime timestamp(0) NOT NULL,
	price_open float8 NULL,
	price_close float8 NULL,
	price_low float8 NULL,
	price_high float8 NULL,
	trading_volume int4 NULL,
	symbol varchar NULL
);
