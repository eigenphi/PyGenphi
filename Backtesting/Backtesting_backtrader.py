#!/usr/bin/env python
# coding: utf-8

# In[1]:


from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime
import os.path
import sys
import random
import math

import backtrader as bt
import backtrader.feeds as btfeed


# In[2]:


class TestStrategy_random(bt.Strategy): #随机买卖

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = self.datas[0].datetime.datetime(0)
        dn = self.datas[0]._name
        print('%s, %s ,%s' % (dt, dn, txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders
        self.order = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % order.executed.price)

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:
            mood_buy = random.choices([0,1], [0.6,0.4])

            # Not yet ... we MIGHT BUY if ...
            if mood_buy == [1]:

                # BUY
                self.log('BUY CREATE', self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

        else:

            # Already in the market ... we might sell
            mood_sell = random.choices([0,1], [0.6,0.4])
            if mood_sell == [1]:
                # SELL
                self.log('SELL CREATE', self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()


# In[3]:


class TestStrategy_triangular(bt.Strategy): #三角套利
    
    def __init__(self):
        self.end = self.datas[0].close[-1]  # holding periods per data

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                print('BUY EXECUTED', order.executed.price)
            elif order.issell():
                print('SELL EXECUTED', order.executed.price)

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            print('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def next(self):
        for i, d in enumerate(self.datas):
            dt, dn = self.datetime.datetime(), d._name
            print('{} {} Close {}'.format(dt, dn, self.datas[i].close[0]))
        
    
        if 1/self.datas[0].close[0]/self.datas[1].close[0]*self.datas[2].close[0] > 1:
            if self.datas[0].close[-1] != self.end:

            # BUY
                print('BUY CREATE,', self.datas[0].close[0], self.datas[1].close[0], self.datas[2].close[0], cerebro.broker.getcash())
                size_A = math.floor(cerebro.broker.getcash()/self.datas[0].close[0])
                self.buy(self.datas[0],price = self.datas[0].close[0], size = size_A)
                size_C = size_A/self.datas[1].close[0]
                cerebro.broker.setcash(cerebro.broker.getcash()+size_C*self.datas[2].close[0])


# In[4]:


if __name__ == '__main__': #triangular arbitrage
    '''
    #When implementing random strategy, use the following codes:
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(TestStrategy_random)
    
    #kwargs for data feeds
    kwargs = {
        'timeframe': bt.TimeFrame.Minutes,
        'compression': 1,
        'fromdate': datetime.datetime(2021, 5, 20, 0, 0), #Define by yourself
        'todate': datetime.datetime(2021, 5, 20, 1, 0), #Define by yourself
        'sessionstart': datetime.time(0, 0), #Use the same time as above
        'sessionend': datetime.time(1, 0), #Same as above
    }

    # Create a Data Feed
    data = bt.feeds.GenericCSVData(
        dataname= 'BTCUSDT.csv', **kwargs
    )

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(100000.0)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    '''
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(TestStrategy_triangular)

    
    #kwargs for data feeds
    kwargs = {
        'timeframe': bt.TimeFrame.Minutes,
        'compression': 1, # The data is already at 5 minute intervals
        'fromdate': datetime.datetime(2021, 5, 20, 0, 0),
        'todate': datetime.datetime(2021, 5, 20, 1, 0),
        'sessionstart': datetime.time(0, 0),
        'sessionend': datetime.time(1, 0),
    }

    # Create a Data Feed
    data1 = bt.feeds.GenericCSVData(
        dataname= 'BTCUSDT.csv', **kwargs
    )
    
    data2 = bt.feeds.GenericCSVData(
        dataname= 'ETHBTC.csv', **kwargs
    )
    
    data3 = bt.feeds.GenericCSVData(
        dataname= 'ETHUSDT.csv', **kwargs
    )


    # Add the Data Feed to Cerebro
    cerebro.adddata(data1)
    
    cerebro.adddata(data2)
    
    cerebro.adddata(data3)


    # Set our desired cash start
    cerebro.broker.setcash(100000.0)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getcash())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getcash())


# In[ ]:




