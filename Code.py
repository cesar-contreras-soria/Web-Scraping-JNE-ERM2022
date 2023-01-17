
#Este codigo unicamente sirve para descargar informacion de los votos en las municipalidades. No se ha incorporado 
#el procedimiento para descargar los votos regionales porque el código sería aún más extenso. Sin embargo, conociendo la estructura
#del presente código, es posible expandirlo fácilmente.

import os
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_experimental_option('prefs', {
        "download.prompt_for_download": False,
        "download.default_directory" : r"C:\Users\CESAR\Desktop\GitHub",
        "savefile.default_directory": r"C:\Users\CESAR\Desktop\GitHub"})

driver_path = r"C:\Program Files\Chromedriver\chromedriver.exe"
os.environ["webdriver.chrome.driver"] = driver_path
driver = webdriver.Chrome(driver_path, chrome_options=options)

#Notar que la página se demora en cargar y el URL cambia cada vez que se selecciona algún ubigeo.
#Eso quiere decir que el driver se va actualizando cada vez.
driver.get('https://resultadoshistorico.onpe.gob.pe/ERM2022/Actas/Ubigeo')
time.sleep(2)

#Departamento
seleccionar_dpto = Select(driver.find_element('id','select_departamento'))
departamento = driver.find_element('id','select_departamento')
dpto_conteo = departamento.find_elements(By.TAG_NAME,'option')

for dpto in range(1,len(dpto_conteo)):
	print(dpto)
	seleccionar_dpto.select_by_index(dpto)
	time.sleep(2)
	#Nuevo driver
	url_dpto = driver.current_url
	driver.get(url_dpto)
	time.sleep(2)

	#Provincia
	seleccionar_prov = Select(driver.find_element('id','cod_prov'))
	provincia = driver.find_element('id','cod_prov')
	prov_conteo = provincia.find_elements(By.TAG_NAME,'option')
	for prov in range(1,len(prov_conteo)):
		print(prov)
		seleccionar_prov.select_by_index(prov)
		time.sleep(2)
		#Nuevo driver
		url_prov = driver.current_url
		driver.get(url_prov)
		time.sleep(2)

		#Distrito
		seleccionar_dist = Select(driver.find_element('id','cod_dist'))
		distrito = driver.find_element('id','cod_dist')
		dist_conteo = distrito.find_elements(By.TAG_NAME,'option')
		for dist in range(1,len(dist_conteo)):
			print(dist)
			seleccionar_dist.select_by_index(dist)
			time.sleep(2)
			#Nuevo driver
			url_dist = driver.current_url
			driver.get(url_dist)
			time.sleep(2)

			#Local
			seleccionar_local = Select(driver.find_element('name','cod_local'))
			local = driver.find_element('name','cod_local')
			local_conteo = local.find_elements(By.TAG_NAME,'option')
			for loc in range(1,len(local_conteo)):
				print("Local ",loc," de ",len(local_conteo))
				seleccionar_local.select_by_index(loc)
				time.sleep(2)
				#Crear base de dato. Dado que en un local existen diversas mesas, se decide realizar la descarga a este nivel.
				base_dato = []
				#Nuevo driver
				url_loc = driver.current_url
				driver.get(url_loc)
				time.sleep(4)

				#Conteo de paginas
				paginas = driver.find_element(By.CLASS_NAME,'pagination')
				pag = paginas.find_elements(By.TAG_NAME,'li')
				time.sleep(2)
				if len(pag)>=2:
					for hoja in range(1,len(pag)+1):
						driver.execute_script("window.scrollTo(0,300)")
						time.sleep(2)
						driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[2]/div/div[2]/div/div[3]/div/ul/li[' + str(hoja) + ']').click()
						time.sleep(3)
						#Conteo de mesas de votacion
						mesas = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[2]/div/div[1]')
						mesas_conteo = mesas.find_elements(By.TAG_NAME,'div')
						for mesa in range(1,len(mesas_conteo)+1):
							driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[2]/div/div[1]/div[' + str(mesa) + ']').click()
							time.sleep(4)
							driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
							time.sleep(6)

							#Datos
							nom_dpto = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[2]/div[2]').text
							nom_prov = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[2]/div[4]').text
							nom_dist = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[2]/div[6]').text
							local_nom = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[2]/div[8]').text
							local_dire = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[2]/div[10]').text
							mesa_num = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[1]/div[2]/div/div[2]').text
							mesa_copia = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[1]/div[2]/div/div[4]').text
							estado_prov = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[1]/div[2]/div/div[6]').text
							elector_hab = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[1]/div[3]/div/div[2]').text
							elector_vot = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[1]/div[3]/div/div[4]').text
							#Algunos no tienen eleccion distrital porque son capitales provinciales. Eg el distrito de Bagua
							tabla_eledis = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[1]/div[3]/div')
							eledis = tabla_eledis.find_elements(By.TAG_NAME,'div')
							if len(eledis)>=5:
								estado_dist = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[1]/div[3]/div/div[6]').text

								#Tabla principal
								tabla_organizacion = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table')
								organizacion = tabla_organizacion.find_elements(By.TAG_NAME,'tr')

								#Datos de votantes
								vota1 = len(organizacion)
								ve_prov = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(vota1) + ']/td[2]').text
								ve_dist = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(vota1) + ']/td[3]').text

								vota2 = vota1 - 1
								vi_prov = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(vota2) + ']/td[2]').text
								vi_dist = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(vota2) + ']/td[3]').text

								vota3 = vota1 - 2
								vn_prov = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(vota3) + ']/td[2]').text
								vn_dist = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(vota3) + ']/td[3]').text

								vota4 = vota1 - 3
								vb_prov = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(vota4) + ']/td[2]').text
								vb_dist = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(vota4) + ']/td[3]').text

								vota5 = vota1 - 4
								vv_prov = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(vota5) + ']/td[2]').text
								vv_dist = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(vota5) + ']/td[3]').text

								#Datos de organizaciones
								for orga in range(2,len(organizacion)-4):
									grupo_nombre = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(orga) + ']/td[2]').text
									grupo_prov = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(orga) + ']/td[3]').text
									grupo_dist = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(orga) + ']/td[4]').text

									base_dato.append([nom_dpto,nom_prov,nom_dist,local_nom,local_dire,mesa_num,mesa_copia,estado_prov,elector_hab,elector_vot,estado_dist,
										ve_prov,ve_dist,vi_prov,vi_dist,vn_prov,vn_dist,vb_prov,vb_dist,vv_prov,vv_dist,grupo_nombre,grupo_prov,grupo_dist])
									df = pd.DataFrame(base_dato,columns=['nom_dpto','nom_prov','nom_dist','local_nom','local_dire','mesa_num','mesa_copia','estado_prov','elector_hab',
										'elector_vot','estado_dist','ve_prov','ve_dist','vi_prov','vi_dist','vn_prov','vn_dist','vb_prov','vb_dist','vv_prov','vv_dist',
										'grupo_nombre','grupo_prov','grupo_dist'])
									df.to_csv('Eleccion_Distrital_' + str(dpto) + '_' + str(prov) + '_' + str(dist) + '_' + str(loc) + '.csv',encoding='utf-8-sig',index=False)

								driver.execute_script("window.scrollTo(0,0)")
								time.sleep(4)

								#Habilitar la pagina. Notar que se regresa a la pagina anterior.
								if hoja>=2:
									url_mesa = driver.current_url
									driver.get(url_mesa)
									driver.execute_script("window.scrollTo(0,300)")
									time.sleep(3)
									driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[2]/div/div[2]/div/div[3]/div/ul/li[' + str(hoja) + ']').click()
									time.sleep(2)
							else:
								estado_dist = "No hay"
								#Tabla principal
								tabla_organizacion = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table')
								organizacion = tabla_organizacion.find_elements(By.TAG_NAME,'tr')

								#Datos de votantes
								vota1 = len(organizacion)
								ve_prov = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(vota1) + ']/td[2]').text
								ve_dist = "No hay"

								vota2 = vota1 - 1
								vi_prov = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(vota2) + ']/td[2]').text
								vi_dist = "No hay"

								vota3 = vota1 - 2
								vn_prov = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(vota3) + ']/td[2]').text
								vn_dist = "No hay"

								vota4 = vota1 - 3
								vb_prov = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(vota4) + ']/td[2]').text
								vb_dist = "No hay"

								vota5 = vota1 - 4
								vv_prov = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(vota5) + ']/td[2]').text
								vv_dist = "No hay"

								#Datos de organizaciones
								for orga in range(2,len(organizacion)-4):
									grupo_nombre = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(orga) + ']/td[2]').text
									grupo_prov = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(orga) + ']/td[3]').text
									grupo_dist = "No hay"

									base_dato.append([nom_dpto,nom_prov,nom_dist,local_nom,local_dire,mesa_num,mesa_copia,estado_prov,elector_hab,elector_vot,estado_dist,
										ve_prov,ve_dist,vi_prov,vi_dist,vn_prov,vn_dist,vb_prov,vb_dist,vv_prov,vv_dist,grupo_nombre,grupo_prov,grupo_dist])
									df = pd.DataFrame(base_dato,columns=['nom_dpto','nom_prov','nom_dist','local_nom','local_dire','mesa_num','mesa_copia','estado_prov','elector_hab',
										'elector_vot','estado_dist','ve_prov','ve_dist','vi_prov','vi_dist','vn_prov','vn_dist','vb_prov','vb_dist','vv_prov','vv_dist',
										'grupo_nombre','grupo_prov','grupo_dist'])
									df.to_csv('Eleccion_Distrital_' + str(dpto) + '_' + str(prov) + '_' + str(dist) + '_' + str(loc) + '.csv',encoding='utf-8-sig',index=False)

								driver.execute_script("window.scrollTo(0,0)")
								time.sleep(4)

								#Habilitar la pagina. Notar que se regresa a la pagina anterior.
								if hoja>=2:
									url_mesa = driver.current_url
									driver.get(url_mesa)
									driver.execute_script("window.scrollTo(0,300)")
									time.sleep(3)
									driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[2]/div/div[2]/div/div[3]/div/ul/li[' + str(hoja) + ']').click()
									time.sleep(2)

				else:
					#Conteo de mesas de votacion
					mesas = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[2]/div/div[1]')
					mesas_conteo = mesas.find_elements(By.TAG_NAME,'div')
					for mesa in range(1,len(mesas_conteo)+1):
						driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[2]/div/div[1]/div[' + str(mesa) + ']').click()
						time.sleep(4)
						driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
						time.sleep(6)

						#Datos
						nom_dpto = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[2]/div[2]').text
						nom_prov = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[2]/div[4]').text
						nom_dist = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[2]/div[6]').text
						local_nom = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[2]/div[8]').text
						local_dire = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[2]/div[10]').text
						mesa_num = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[1]/div[2]/div/div[2]').text
						mesa_copia = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[1]/div[2]/div/div[4]').text
						estado_prov = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[1]/div[2]/div/div[6]').text
						elector_hab = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[1]/div[3]/div/div[2]').text
						elector_vot = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[1]/div[3]/div/div[4]').text
						#Algunos no tienen eleccion distrital porque son capitales provinciales. Eg el distrito de Bagua
						tabla_eledis = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[1]/div[3]/div')
						eledis = tabla_eledis.find_elements(By.TAG_NAME,'div')
						if len(eledis)>=5:
							estado_dist = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[1]/div[3]/div/div[6]').text
							#Tabla principal
							tabla_organizacion = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table')
							organizacion = tabla_organizacion.find_elements(By.TAG_NAME,'tr')

							#Datos de votantes
							vota1 = len(organizacion)
							ve_prov = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(vota1) + ']/td[2]').text
							ve_dist = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(vota1) + ']/td[3]').text

							vota2 = vota1 - 1
							vi_prov = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(vota2) + ']/td[2]').text
							vi_dist = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(vota2) + ']/td[3]').text

							vota3 = vota1 - 2
							vn_prov = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(vota3) + ']/td[2]').text
							vn_dist = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(vota3) + ']/td[3]').text

							vota4 = vota1 - 3
							vb_prov = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(vota4) + ']/td[2]').text
							vb_dist = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(vota4) + ']/td[3]').text

							vota5 = vota1 - 4
							vv_prov = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(vota5) + ']/td[2]').text
							vv_dist = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(vota5) + ']/td[3]').text

							#Datos de organizaciones
							for orga in range(2,len(organizacion)-4):
								grupo_nombre = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(orga) + ']/td[2]').text
								grupo_prov = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(orga) + ']/td[3]').text
								grupo_dist = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(orga) + ']/td[4]').text

								base_dato.append([nom_dpto,nom_prov,nom_dist,local_nom,local_dire,mesa_num,mesa_copia,estado_prov,elector_hab,elector_vot,estado_dist,
									ve_prov,ve_dist,vi_prov,vi_dist,vn_prov,vn_dist,vb_prov,vb_dist,vv_prov,vv_dist,grupo_nombre,grupo_prov,grupo_dist])
								df = pd.DataFrame(base_dato,columns=['nom_dpto','nom_prov','nom_dist','local_nom','local_dire','mesa_num','mesa_copia','estado_prov','elector_hab',
									'elector_vot','estado_dist','ve_prov','ve_dist','vi_prov','vi_dist','vn_prov','vn_dist','vb_prov','vb_dist','vv_prov','vv_dist',
									'grupo_nombre','grupo_prov','grupo_dist'])
								df.to_csv('Eleccion_Distrital_' + str(dpto) + '_' + str(prov) + '_' + str(dist) + '_' + str(loc) + '.csv',encoding='utf-8-sig',index=False)

							driver.execute_script("window.scrollTo(0,0)")
							time.sleep(4)

						else:
							estado_dist = "No hay"
							#Tabla principal
							tabla_organizacion = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table')
							organizacion = tabla_organizacion.find_elements(By.TAG_NAME,'tr')

							#Datos de votantes
							vota1 = len(organizacion)					
							ve_prov = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(vota1) + ']/td[2]').text
							ve_dist = "No hay"

							vota2 = vota1 - 1
							vi_prov = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(vota2) + ']/td[2]').text
							vi_dist = "No hay"

							vota3 = vota1 - 2
							vn_prov = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(vota3) + ']/td[2]').text
							vn_dist = "No hay"

							vota4 = vota1 - 3
							vb_prov = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(vota4) + ']/td[2]').text
							vb_dist = "No hay"

							vota5 = vota1 - 4
							vv_prov = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(vota5) + ']/td[2]').text
							vv_dist = "No hay"

							#Datos de organizaciones
							for orga in range(2,len(organizacion)-4):		
								grupo_nombre = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(orga) + ']/td[2]').text
								grupo_prov = driver.find_element('xpath','/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-ubig/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div[2]/div/div/table/tbody/tr[' + str(orga) + ']/td[3]').text
								grupo_dist = "No hay"

								base_dato.append([nom_dpto,nom_prov,nom_dist,local_nom,local_dire,mesa_num,mesa_copia,estado_prov,elector_hab,elector_vot,estado_dist,
									ve_prov,ve_dist,vi_prov,vi_dist,vn_prov,vn_dist,vb_prov,vb_dist,vv_prov,vv_dist,grupo_nombre,grupo_prov,grupo_dist])
								df = pd.DataFrame(base_dato,columns=['nom_dpto','nom_prov','nom_dist','local_nom','local_dire','mesa_num','mesa_copia','estado_prov','elector_hab',
									'elector_vot','estado_dist','ve_prov','ve_dist','vi_prov','vi_dist','vn_prov','vn_dist','vb_prov','vb_dist','vv_prov','vv_dist',
									'grupo_nombre','grupo_prov','grupo_dist'])
								df.to_csv('Eleccion_Distrital_' + str(dpto) + '_' + str(prov) + '_' + str(dist) + '_' + str(loc) + '.csv',encoding='utf-8-sig',index=False)

							driver.execute_script("window.scrollTo(0,0)")
							time.sleep(4)

				#Regresar a local
				driver.get(url_dist)
				time.sleep(5)
				seleccionar_local = Select(driver.find_element('name','cod_local'))

			#Regresar a distrito
			driver.get(url_prov)
			time.sleep(2)
			seleccionar_dist = Select(driver.find_element('id','cod_dist'))

		#Regresar a provincia
		driver.get(url_dpto)
		time.sleep(2)
		seleccionar_prov = Select(driver.find_element('id','cod_prov'))

	#Regresar a departamento
	driver.get('https://resultadoserm2022.onpe.gob.pe/ERM2022/Actas/Ubigeo')
	time.sleep(2)
	seleccionar_dpto = Select(driver.find_element('id','select_departamento'))

driver.close()