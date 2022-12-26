# import library
import pandas as pd
import streamlit as st
import plotly.express as px
import geopandas as gpd

def main():
  # import data
  data = pd.read_csv('reg_data_clean.csv')
  df_geo = gpd.read_file('indonesia.geojson')

  # page configuration
  st.set_page_config(page_title = "LTFS Batch 2 Analysis",
                     page_icon = ":bar_chart:",
                     layout = "wide")

  # SIDEBAR
  st.sidebar.header("Filter Data")
  uni_hs = st.sidebar.multiselect(
      "Berdasarkan Perguruan Tinggi atau Sekolah Menengah:",
      options = data['uni_or_hs'].unique(),
      default = data['uni_or_hs'].unique()
  )

  data_filter = data.query(
      "uni_or_hs == @uni_hs"
  )

  # MAIN BODY
  st.write('''
      # Lead The Future Scholarship Batch 2 : Analisis Pendaftar
      Dashboard ini adalah analisis dari pendaftar Lead The Future Scholarship Batch 2. Analisis terdiri dari Exploratory Data Analysis,
      analisis dari segi implementasi marketing dan lainnya. 
  ''')

  st.write('''
      ## Dataset
      Data yang digunakan berasal dari data yang dikumpulkan dari google form pendaftaran dari dua email (email Ka Kevin dan Ka Debora) yang
      dikombinasikan dan dibersihkan untuk kemudahan analisis dan konsistensi struktur
  ''')

  st.dataframe(data_filter)

  st.write('### Penjelasan Data:')
  hide_table_row_index = """
              <style>
              thead tr th:first-child {display:none}
              tbody th {display:none}
              </style>
              """
  st.markdown(hide_table_row_index, unsafe_allow_html=True)
  st.table(pd.DataFrame({
      'Judul Kolom': ['time',
                      'email',
                      'name',
                      'number',
                      'gender',
                      'age',
                      'province',
                      'city_regency',
                      'birth_date',
                      'schreg_reason',
                      'uni_or_hs',
                      'hs_type',
                      'hs_name',
                      'hs_grade',
                      'uni_type',
                      'uni_sector',
                      'uni_name',
                      'uni_level',
                      'uni_major',
                      'uni_year_enlist',
                      'ig_username',
                      'schreg_info_source',
                      'inspiration_story'],
      'Penjelasan Isi Kolom': ['Waktu pendaftar melakukan submit',
                               'Email yang digunakan pendaftar untuk melakukan submit',
                               'Nama pendaftar',
                               'Nomor telepon Whatsapp pendaftar',
                               'Jenis kelamin pendaftar',
                               'Umur pendaftar',
                               'Provinsi asal dari pendaftar',
                               'Domisili dalam tingkat kota atau kabupaten dari pendaftar',
                               'Tanggal lahir dari pendaftar',
                               'Alasan kenapa pendaftar mendaftar LTFS, alasan terkategorisasi',
                               'Label untuk menandakan apakah pendaftar berasal dari Perguruan Tinggi atau Sekolah Menengah',
                               'Tipe dari Sekolah Menengah pendaftar',
                               'Nama Sekolah Menengah pendaftar',
                               'Kelas pendaftar di Sekolah Menengah',
                               'Tipe dari Perguruan Tinggi pendaftar',
                               'Perguruan Tinggi Negeri atau Swasta',
                               'Nama Perguruan Tinggi',
                               'Tingkat dari Perguruan Tinggi pendaftar, jangkauan dari D1 sampai S1',
                               'Fakultas dan jurusan dari pendaftar',
                               'Tahun masuk dari pendaftar pada Perguruan Tinggi',
                               'Username Instagram dari pendaftar',
                               'Asal sosial media dimana pendaftar mendapatkan informasi mengenai beasiswa dan pendaftaran',
                               'Apakah pendaftar mencantumkan kisah inspiratif mengenai pengalaman memimpin, ya = 1, tidak = 0'],
  }))

  st.write('## Exploratory Data Analysis')
  df_pendaftar_prov = data_filter[['name','province']].replace('Bangka Belitung', 'Bangka-Belitung').replace('DKI Jakarta', 'Jakarta Raya').groupby('province').count()
  df_merged = df_geo.merge(df_pendaftar_prov, how='inner', left_on='state', right_on='province')
  df_merged = df_merged[['state','geometry','name']].rename(columns = {'name':'Banyak Pendaftar'})

  fig = px.choropleth(df_merged, geojson=df_merged.geometry,
                      locations=df_merged.index,
                      color='Banyak Pendaftar',
                      color_continuous_scale='Jet',
                      hover_name = 'state')

  fig.update_geos(fitbounds='locations', visible=False)

  fig.update_layout(height=450)
  fig.update_layout(
      margin=dict(l=20, r=20, t=20, b=20),
      paper_bgcolor='rgb(14,17,23)',
      plot_bgcolor ='rgb(14,17,23)' )

  col1, col2 = st.columns([5, 1])

  col1.subheader("Banyak Pendaftar tiap Provinsi di Indonesia")
  col1.plotly_chart(fig,use_container_width=True,height=450)

  col2.subheader("Jumlah Tiap Provinsi")
  col2.write(df_pendaftar_prov)

  col1, col2, col3, col4 = st.columns(4)
  max_index = df_pendaftar_prov['name'].idxmax()
  col1.metric("Provinsi dengan Pendaftar Terbanyak", "Provinsi " + max_index)
  col2.metric("Pendaftar dari Perguruan Tinggi", int(data_filter[data_filter['uni_or_hs'] == 'uni']['name'].count()), str(round(int(data_filter[data_filter['uni_or_hs'] == 'uni']['name'].count()) / int(data['name'].count()) * 100))  + '%')
  col3.metric("Pendaftar dari Sekolah Menengah", int(data_filter[data_filter['uni_or_hs'] == 'hs']['name'].count()), str(round(int(data_filter[data_filter['uni_or_hs'] == 'hs']['name'].count()) / int(data['name'].count()) * 100))  + '%')
  col4.metric("Pendaftar dari Perguruan Tinggi Luar Negeri", str(int(data_filter[data_filter['province'] == 'Luar Negeri']['name'].count())))

  st.write('### Analisis Demografi')
  col1, col2= st.columns(2)
  fig1 = px.pie(data_filter[['gender','name']].groupby('gender').count().rename(columns = {'name':'Banyak Pendaftar'}),values = 'Banyak Pendaftar', names = data_filter[['gender','name']].groupby('gender').count().index, title = "Pembagian Pendaftar Berdasarkan Jenis Kelamin")
  col1.plotly_chart(fig1)
  fig2 = px.pie(data_filter[['age','name']].groupby('age').count().rename(columns = {'name':'Banyak Pendaftar'}),values = 'Banyak Pendaftar', names = data_filter[['age','name']].groupby('age').count().index, title = "Pembagian Pendaftar Berdasarkan Umur")
  col2.plotly_chart(fig2)

  col1, col2= st.columns(2)
  fig1 = px.pie(data_filter[['schreg_reason','name']].groupby('schreg_reason').count().rename(columns = {'name':'Banyak Pendaftar'}),values = 'Banyak Pendaftar', names = data_filter[['schreg_reason','name']].groupby('schreg_reason').count().index, title = "Pembagian Pendaftar Berdasarkan Alasan Mendaftar")
  col1.plotly_chart(fig1)
  fig2 = px.pie(data_filter[['city_regency','name']].replace('Kota Bandung','Bandung').replace('Kota Medan', 'Medan').replace('Kota Bekasi','Bekasi').replace('Kota Malang','Malang').groupby('city_regency').count().rename(columns = {'name':'Banyak Pendaftar'}).nlargest(20, 'Banyak Pendaftar'),values = 'Banyak Pendaftar', names = data_filter[['city_regency','name']].replace('Kota Bandung','Bandung').replace('Kota Medan', 'Medan').replace('Kota Bekasi','Bekasi').replace('Kota Malang','Malang').groupby('city_regency').count().nlargest(20, 'name').index, title = "Pembagian Pendaftar Berdasarkan Kabupaten dan Kota (Top 20 Data)")
  col2.plotly_chart(fig2)

  st.write('### Analisis Pendaftar Sekolah Menengah')
  col1, col2= st.columns(2)
  fig1 = px.pie(data_filter[['hs_type','name']].groupby('hs_type').count().rename(columns = {'name':'Banyak Pendaftar'}),values = 'Banyak Pendaftar', names = data_filter[['hs_type','name']].groupby('hs_type').count().index, title = "Pembagian Pendaftar Berdasarkan Jenis Sekolah Menengah")
  col1.plotly_chart(fig1)
  fig2 = px.pie(data_filter[['hs_grade','name']].groupby('hs_grade').count().rename(columns = {'name':'Banyak Pendaftar'}),values = 'Banyak Pendaftar', names = data_filter[['hs_grade','name']].groupby('hs_grade').count().index, title = "Pembagian Pendaftar Berdasarkan Kelas Sekolah Menengah")
  col2.plotly_chart(fig2)

  st.write('### Analisis Pendaftar Perguruan Tinggi')
  col1, col2= st.columns(2)
  fig1 = px.pie(data_filter[['uni_type','name']].groupby('uni_type').count().rename(columns = {'name':'Banyak Pendaftar'}),values = 'Banyak Pendaftar', names = data_filter[['uni_type','name']].groupby('uni_type').count().index, title = "Pembagian Pendaftar Berdasarkan Jenis Perguruan Tinggi")
  col1.plotly_chart(fig1)
  fig2 = px.pie(data_filter[['uni_sector','name']].groupby('uni_sector').count().rename(columns = {'name':'Banyak Pendaftar'}),values = 'Banyak Pendaftar', names = data_filter[['uni_sector','name']].groupby('uni_sector').count().index, title = "Pembagian Pendaftar Berdasarkan Sektor Perguruan Tinggi")
  col2.plotly_chart(fig2)

  col1, col2= st.columns(2)
  fig1 = px.pie(data_filter[['uni_level','name']].groupby('uni_level').count().rename(columns = {'name':'Banyak Pendaftar'}),values = 'Banyak Pendaftar', names = data_filter[['uni_level','name']].groupby('uni_level').count().index, title = "Pembagian Pendaftar Berdasarkan Tingkat Perguruan Tinggi")
  col1.plotly_chart(fig1)
  fig2 = px.pie(data_filter[['uni_name','name']].replace('Universitas Sriwijaya ','Universitas Sriwijaya').replace('Universitas Pendidikan Indonesia ','Universitas Pendidikan Indonesia').groupby('uni_name').count().rename(columns = {'name':'Banyak Pendaftar'}).nlargest(20, 'Banyak Pendaftar'),values = 'Banyak Pendaftar', names = data_filter[['uni_name','name']].replace('Universitas Sriwijaya ','Universitas Sriwijaya').replace('Universitas Pendidikan Indonesia ','Universitas Pendidikan Indonesia').groupby('uni_name').count().nlargest(20, 'name').index, title = "Pembagian Pendaftar Berdasarkan Perguruan Tinggi (Top 20 Data)")
  col2.plotly_chart(fig2)

  col1, col2= st.columns(2)
  fig1 = px.pie(data_filter[['uni_major','name']].groupby('uni_major').count().rename(columns = {'name':'Banyak Pendaftar'}).nlargest(20, 'Banyak Pendaftar'),values = 'Banyak Pendaftar', names = data_filter[['uni_major','name']].groupby('uni_major').count().nlargest(20, 'name').index, title = "Pembagian Pendaftar Berdasarkan Jurusan dan Fakultas (Top 20 Data)")
  col1.plotly_chart(fig1)
  fig2 = px.pie(data_filter[['uni_year_enlist','name']].groupby('uni_year_enlist').count().rename(columns = {'name':'Banyak Pendaftar'}),values = 'Banyak Pendaftar', names = data_filter[['uni_year_enlist','name']].groupby('uni_year_enlist').count().index, title = "Pembagian Pendaftar Berdasarkan Angkatan di Perguruan Tinggi")
  col2.plotly_chart(fig2)

  st.write('### Analisis Keefektifan Sosial Media')
  col1, col2= st.columns(2)
  fig1 = px.pie(data_filter[['schreg_info_source','name']].groupby('schreg_info_source').count().rename(columns = {'name':'Banyak Pendaftar'}),values = 'Banyak Pendaftar', names = data_filter[['schreg_info_source','name']].groupby('schreg_info_source').count().index, title = "Informasi dari Sosial Media Tentang LTFS Batch 2")
  col1.plotly_chart(fig1)
  fig2 = px.pie(data_filter[['inspiration_story','name']].replace(1,'Ikut').replace(0,'Tidak Ikut').groupby('inspiration_story').count().rename(columns = {'name':'Banyak Pendaftar'}),values = 'Banyak Pendaftar', names = data_filter[['inspiration_story','name']].replace(1,'Ikut').replace(0,'Tidak Ikut').groupby('inspiration_story').count().index, title = "Banyak Peserta yang Mengikuti Campaign Kisah Inspiratif")
  col2.plotly_chart(fig2)

  data_filter['time'] = pd.to_datetime(data_filter['time'])
  data_filter['MonthDay'] = data_filter['time'].dt.strftime('%y-%m-%d')
  date_data = data_filter[['name', 'MonthDay']].groupby('MonthDay').count().rename(columns = {'name':'Banyak Pendaftar'})
  fig = px.line(date_data, title = "Frekuensi Pendaftar Selama Berlangsungnya Kampanye",height = 500)
  st.plotly_chart(fig,use_container_width=True)

if __name__ == "__main__":
  main()


