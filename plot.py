#!/usr/bin/env python3

import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

fname = "COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"

def parse_date(x):
    return datetime.datetime.strptime(x, "%m/%d/%y")

if __name__ == '__main__':
    with open(fname) as f:
        lines_iter = iter(f)
        header = next(lines_iter)
        header = header.rstrip().split(',')
        COUNTRY_ID = 1
        TIMESERIES_ID0 = 4
        assert header[0] == 'Province/State'
        assert header[COUNTRY_ID] == 'Country/Region'
        assert header[2] == 'Lat'
        assert header[3] == 'Long'
        dates = [
            datetime.datetime.strptime(x, "%m/%d/%y")
            for x in header[TIMESERIES_ID0:]
        ]

        # Filter
        data = []
        countries = ['Switzerland', 'Italy', 'Greece']
        for line in lines_iter:
            line = line.rstrip().split(',')
            country = line[COUNTRY_ID]
            if country in countries:
                ts = [ int(x) for x in line[TIMESERIES_ID0:] ]
                data.append((country, ts))


        # Plot
        (fig, (ax_log, ax)) = plt.subplots(2,1, figsize=(7,9))
        ax.set_xlabel("Time")
        ax.set_ylabel("Cases")
        ax.set_title("COVID-19: Confirmed cases")
        ax.grid(True)

        ax_log.set_xlabel("Time")
        ax_log.set_ylabel("Cases (log scale)")
        ax_log.set_title("COVID-19: Confirmed cases (log scale)")
        ax_log.grid(True)

        #dt_fmt = mdates.DateFormatter('%d/%m')
        #ax.xaxis.set_major_formatter(dt_fmt)
        locator = mdates.AutoDateLocator(minticks=5, maxticks=10)
        formatter = mdates.ConciseDateFormatter(locator)
        days_loc = mdates.DayLocator()
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)
        ax.xaxis.set_minor_locator(days_loc)

        locator = mdates.AutoDateLocator(minticks=5, maxticks=10)
        formatter = mdates.ConciseDateFormatter(locator)
        days_loc = mdates.DayLocator()
        ax_log.xaxis.set_major_locator(locator)
        ax_log.xaxis.set_major_formatter(formatter)
        ax_log.xaxis.set_minor_locator(days_loc)

        T0 = 8
        for (country, ts) in data:
            ax.plot(dates[T0:], ts[T0:], label=country)
            ax.annotate("%s" % (ts[-1]), xy=(dates[-1], ts[-1]))
            ax_log.semilogy(dates[T0:], ts[T0:], label=country)
            ax_log.annotate("%s" % (ts[-1]), xy=(dates[-1], ts[-1]))
        ax.legend()
        ax_log.legend()

        plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=.3)
        fig.savefig('covid19-countries-confirmed.pdf')
        fig.savefig('covid19-countries-confirmed.png')
