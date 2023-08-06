import requests, json
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots

pd.options.display.float_format = '{:,.2f}'.format
pd.set_option('mode.chained_assignment', None)

url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Origin': 'http://data.krx.co.kr',
    'Referer': 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020201',
}


# 마스터, 시세 크롤링 모듈
def krx_df(data):
    raw = requests.post(url, headers=headers, data=data).text
    rst = json.loads(raw)['OutBlock_1']
    ln = []
    for r in rst:
        ln.append([c for c in r.values()])
    df = pd.DataFrame(ln)
    df.columns = r.keys()
    return df


# 종목 마스터 크롤링
def make_master():
    data = {
        'menuId': 'MDC0201020201',
        'bld': 'dbms/MDC/STAT/standard/MDCSTAT01901',
        'locale': 'ko_KR',
        'mktId': 'ALL',
        'share': '1',
        'csvxls_isNo': 'false',
    }
    krx_master = krx_df(data)
    # 유, 코 보통주만 발라냄
    master = krx_master.query(
        'SECUGRP_NM=="주권"' and 'MKT_TP_NM in ("KOSPI","KOSDAQ")' and 'KIND_STKCERT_TP_NM=="보통주"').copy()
    return master


# 시세 데이터 크롤링
def make_price(start_date=None, end_date=None):
    end_date = pd.to_datetime(end_date).strftime('%Y%m%d') if end_date else pd.Timestamp.today().strftime('%Y%m%d')
    start_date = pd.to_datetime(start_date).strftime('%Y%m%d') if start_date else (
                pd.Timestamp.today() - pd.DateOffset(years=1)).strftime('%Y%m%d')
    data = {
        'menuId': 'MDC0201020201',
        'bld': 'dbms/MDC/STAT/standard/MDCSTAT01501',
        'locale': 'ko_KR',
        'mktId': 'ALL',
        'trdDd': '20230220',
        'share': '1',
        'csvxls_isNo': 'false',
    }
    dates = pd.date_range(start=start_date, end=end_date, freq='B')
    acc_price = pd.DataFrame()
    for i, d in enumerate(dates):
        print('\r', '{}% : {}'.format(int((i + 1) / len(dates) * 100), d.strftime('%Y%m%d')), end=' ')
        data['trdDd'] = d.strftime('%Y%m%d')
        daily_price = krx_df(data)
        daily_price['DATE'] = d.strftime('%Y-%m-%d')
        acc_price = pd.concat([acc_price, daily_price], axis=0)
    acc_price['DATE'] = pd.to_datetime(acc_price['DATE'])
    acc_price['TDD_CLSPRC'] = pd.to_numeric(acc_price['TDD_CLSPRC'].replace(',','', regex=True), errors='coerce')
    acc_price['ACC_TRDVOL'] = pd.to_numeric(acc_price['ACC_TRDVOL'].replace(',','', regex=True), errors='coerce')
    acc_price['ACC_TRDVAL'] = pd.to_numeric(acc_price['ACC_TRDVAL'].replace(',','', regex=True), errors='coerce')

    return acc_price


class VolumeSimulation:
    def __init__(self):
        self.days = None
        self.start_6m = None
        self.end_6m = None
        self.master = make_master()
        self.all_price = None
        self.cr_dict = {
            'price': 'TDD_CLSPRC',
            'volume': 'ACC_TRDVOL',
            'value': 'ACC_TRDVAL',
        }

    # 데이터 준비
    def get_data(self, start_date=None, end_date=None):
        self.all_price = make_price(start_date, end_date)

    # 6개월 계산
    def cal_dates(self, m=6):
        daily = pd.DataFrame()
        daily['KRX'] = self.all_price.groupby(by='DATE')['ACC_TRDVOL'].sum()
        daily.dropna(inplace=True)
        daily.index = pd.to_datetime(daily.index)
        daily = daily[daily['KRX']>0]
        self.all_price = self.all_price[self.all_price['DATE'].isin(daily.index)]
        self.end_6m = daily.index[-1].date()  # 데이터상 마지막 일자
        self.start_6m = (self.end_6m - pd.DateOffset(months=(5)) - pd.offsets.MonthBegin()).date()  # 6개월전 1일
        self.days = len(daily[self.start_6m:self.end_6m])  # 6개월간 거래일수 계산

    # plotly 차트
    def chart(self, df):
        df_ = df.iloc[-self.days:].copy()

        figs = make_subplots(specs=[[{'secondary_y': True}]])

        fig = px.area(df_[['N', 'K']])
        fig['data'][0]['line']['color'] = 'rgba(255, 153, 0,.5)'
        fig['data'][0]['fillcolor'] = 'rgba(255, 153, 0,.4)'
        fig['data'][1]['line']['color'] = 'rgba(0, 204, 0,.5)'
        fig['data'][1]['fillcolor'] = 'rgba(0, 204, 0,.4)'

        fig2 = px.line(df_['MA%'])
        fig2['data'][0]['line']['color'] = 'rgba(200,100,100,1)'
        fig2['data'][0]['line']['width'] = 3
        fig2.update_traces(yaxis='y2')

        figs.add_traces(fig.data + fig2.data)
        figs.update_layout(width=900, height=300, margin=dict(l=20, r=20, t=20, b=20))
        all_date_range = pd.date_range(df_.index[0], df_.index[-1])
        figs.update_xaxes(
            rangebreaks=[
                dict(bounds=["sat", "mon"]),  # hide weekends
                dict(values=list(all_date_range[~all_date_range.isin(df_.index)]))
            ]
        )
        figs.show()

    # plotly 차트
    def chart_limit(self, df):
        df_ = df.iloc[-self.days:].copy()

        fig = px.bar(df_['Limit'])
        fig.update_layout(width=900, height=300, margin=dict(l=20, r=20, t=20, b=20))
        all_date_range = pd.date_range(df_.index[0], df_.index[-1])
        fig.update_xaxes(
            rangebreaks=[
                dict(bounds=["sat", "mon"]),
                dict(values=list(all_date_range[~all_date_range.isin(df_.index)]))
            ]
        )
        fig.show()

    # 시뮬레이션 준비
    def simulation_ready(self, cd, base_limit=.5):
        sim = pd.DataFrame()
        sim = self.all_price[self.all_price['ISU_SRT_CD']==cd][['ACC_TRDVOL']].copy()
        sim.rename(columns={'ACC_TRDVOL':'KRX'}, inplace=True)
        sim.index = self.all_price[self.all_price['ISU_SRT_CD']==cd]['DATE']
        sim.dropna(inplace=True)
        sim.index = pd.to_datetime(sim.index)
        sim['N'] = sim['KRX'] * np.random.rand(len(sim['KRX'])) * base_limit   # KRX 거래량의 __% 이내에서 랜덤 발생
        sim['K'] = sim['KRX'] - sim['N']    # 나눠먹은 후 K 거래량
        sim['Daily%'] = sim['N']/sim['K']
        sim['MA%'] = sim['N'].rolling(self.days).sum()/sim['K'].rolling(self.days).sum()
        return sim

    # 시뮬레이션 실행
    def simulation_plain(self, cd, base_limit=.5, threshold=.29, adj_limit=.2):
        sim = self.simulation_ready(cd, base_limit)
        sim['Limit'] = base_limit    # 기본 한도 50%
        for i in range(self.days, len(sim)):
            sim['N'].iloc[i] = sim['KRX'].iloc[i] * np.random.rand() * sim['Limit'].iloc[i-1]   # KRX 거래량의 __% 이내에서 랜덤 발생
            sim['K'].iloc[i] = sim['KRX'].iloc[i] - sim['N'].iloc[i]    # 나눠먹은 후 K 거래량
            sim['MA%'].iloc[i] = sim['N'].iloc[i-self.days:i].sum()/sim['K'].iloc[i-self.days:i].sum()
            if sim['MA%'].iloc[i] > threshold:    # MA %가 __ 이상이면
                sim['Limit'].iloc[i] = adj_limit    # Limit을 __ 으로 설정
        sim['Daily%'] = sim['N']/sim['K']    # 일별 점유율
        return sim

    # 시뮬레이션 실행
    def simulation_var(self, cd, base_limit=.5, threshold=.4, adj_limit=.2, end_threshold=.25, end_adj_limit=.1):
        sim = self.simulation_ready(cd, base_limit)
        sim['Limit'] = base_limit    # 기본 한도 50%
        for i in range(self.days, len(sim)):
            sim['N'].iloc[i] = sim['KRX'].iloc[i] * np.random.rand() * sim['Limit'].iloc[i-1]   # KRX 거래량의 __% 이내에서 랜덤 발생
            sim['K'].iloc[i] = sim['KRX'].iloc[i] - sim['N'].iloc[i]    # 나눠먹은 후 K 거래량
            sim['MA%'].iloc[i] = sim['N'].iloc[i-self.days:i].sum()/sim['K'].iloc[i-self.days:i].sum()
            if sim.index[i].day < 21:    # 매월 20일 까지
                if sim['MA%'].iloc[i] > threshold:    # MA %가 __ 이상이면
                    sim['Limit'].iloc[i] = adj_limit    # Limit을 __ 으로 설정
            else:    # 21일 부터는
                if sim['MA%'].iloc[i] > end_threshold:    # MA %가 __ 이상이면
                    sim['Limit'].iloc[i] = end_adj_limit    # Limit을 __ 으로 설정

        sim['Daily%'] = sim['N']/sim['K']    # 일별 점유율
        return sim

    # 지수 구성종목
    def constituents(self, idx='KOSPI200'):
        idx = idx.replace(' ', '')
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT00601',
            'locale': 'ko_KR',
            'indIdx': '1' if idx[:5] == 'KOSPI' else '2',
            'indIdx2': '028' if idx == 'KOSPI200' else '203',
            'trdDd': self.end_6m.strftime('%Y%m%d'),
        }
        raw = requests.post(url, headers=headers, data=data).text
        rst = json.loads(raw)['output']
        ln = []
        for r in rst:
            ln.append([c for c in r.values()])
        df = pd.DataFrame(ln)
        df.columns = r.keys()
        return list(df['ISU_SRT_CD'])

    # N종목 시뮬레이션 준비
    def top_n(self, mkt='KOSPI', n=200):
        top_const = list(self.all_price[(self.all_price['DATE'] > "2022-01-01") & (self.all_price['DATE'] < "2022-12-31") & (
            self.all_price['ISU_SRT_CD'].isin(self.master.query('MKT_TP_NM=="{}"'.format(mkt))['ISU_SRT_CD']))].groupby(by='ISU_SRT_CD')[
                                 'ACC_TRDVAL'].sum().sort_values(ascending=False)[:n].index)
        idx_ = 'KOSPI200' if mkt=='KOSPI' else 'KOSDAQ150'
        idx_const = self.constituents(idx=idx_)
        # merge
        agg_const = list(set(top_const).union(set(idx_const)))
        print(mkt, ':', len(agg_const))
        return agg_const

    # N종목 시뮬레이션
    def simulation_n(self, all_stocks, base_limit=.5, threshold=.295, adj_limit=.2):
        agg_sim = pd.DataFrame()
        for i, cd in enumerate(all_stocks):
            print('\r', '{}% [{}]'.format(int(i/len(all_stocks)*100), cd), end='  ')
            sim = self.simulation(cd, base_limit, threshold, adj_limit)
            sim['symbol'] = cd
            agg_sim = pd.concat([agg_sim, sim])
        agg_sim.sort_values(by='DATE')
        agg_vol = agg_sim.groupby(['DATE']).sum(numeric_only=True)

        daily = pd.DataFrame()
        daily['KRX'] = self.all_price.groupby(by='DATE')['ACC_TRDVOL'].sum()
        daily.dropna(inplace=True)
        daily.index = pd.to_datetime(daily.index)
        daily['N'] = agg_vol['N']
        daily['K'] = daily['KRX'] - daily['N']  # 나눠먹은 후 K 거래량
        daily['Daily%'] = daily['N'] / daily['K']
        daily['MA%'] = daily['N'].rolling(self.days).sum() / daily['K'].rolling(self.days).sum()
        return daily

    # 가격 변동성
    def volatility(self, cd, criteria):
        df = self.all_price[self.all_price['ISU_SRT_CD']==cd][['TDD_CLSPRC','ACC_TRDVOL','ACC_TRDVAL']].copy()
        df.index = self.all_price[self.all_price['ISU_SRT_CD']==cd]['DATE']
        df.dropna(inplace=True)
        df.index = pd.to_datetime(df.index)
        df['Volatility'] = df[self.cr_dict[criteria]].pct_change().rolling(self.days).std()
        return df

    def chart_volatility(self, df, criteria):
        df_ = df.iloc[-self.days:].copy()

        figs = make_subplots(specs=[[{'secondary_y': True}]])

        fig = px.area(df_[self.cr_dict[criteria]])
        fig['data'][0]['line']['color'] = 'rgba(50,50,200,.3)'
        fig['data'][0]['fillcolor'] = 'rgba(50,50,200,.2)'

        fig2 = px.line(df_['Volatility'])
        fig2['data'][0]['line']['color'] = 'rgba(200,100,100,1)'
        fig2['data'][0]['line']['width'] = 3
        fig2.update_traces(yaxis='y2')

        figs.add_traces(fig.data + fig2.data)
        figs.update_layout(width=900, height=300, margin=dict(l=20, r=20, t=20, b=20))
        all_date_range = pd.date_range(df_.index[0], df_.index[-1])
        figs.update_xaxes(
            rangebreaks=[
                dict(bounds=["sat", "mon"]),
                dict(values=list(all_date_range[~all_date_range.isin(df_.index)]))
            ]
        )
        figs.show()
