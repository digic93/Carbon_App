from django.test import TestCase
from company.models import Country, BranchOffice
from emission_source.models import TypeUnitMeasurement, UnitMeasurement, EmissionSource, EmissionFactor, HistoryEmissionFactor, GreenhouseGas

class AbstractEmissionSourceTestCase(TestCase):
    def create_types_unit_measurements(self):
        TypeUnitMeasurement.objects.create(name ="Masa por Energia")
        TypeUnitMeasurement.objects.create(name = "Masa por Galón")

    def create_units_measurements(self):
        mass_per_energy =  TypeUnitMeasurement.objects.get(name ="Masa por Energia")
        mass_per_gallon =  TypeUnitMeasurement.objects.get(name ="Masa por Galón")
        
        UnitMeasurement.objects.create(
            name = "Kilogramo CO2 por Kilovatio hora",
            unit = "kg CO2/kWh",
            type_unit = mass_per_energy,
            description = "Cantidad de CO2 en Kilogramo producido por consumo de energía en Kilovatios hora."
        )

        UnitMeasurement.objects.create(
            name = "Kilogramo CO2 por galón",
            unit = "kg CO2/gal",
            type_unit = mass_per_gallon,
            description = "Cantidad de CO2 en Kilogramo producido por galón de combustible."
        )

        UnitMeasurement.objects.create(
            name = "Kilogramo CH4 por galón",
            unit = "kg CH4/gal",
            type_unit = mass_per_gallon,
            description = "Cantidad de CH4 en Kilogramo producido por galón de combustible."
        )

        UnitMeasurement.objects.create(
            name = "Kilogramo NO2 por galón",
            unit = "kg NO2/gal",
            type_unit = mass_per_gallon,
            description = "Cantidad de NO2 en Kilogramo producido por galón de combustible."
        )

    def create_emission_sources(self):
        EmissionSource.objects.create(name="Electricidad")
        EmissionSource.objects.create(name="Diesel Movil")
        EmissionSource.objects.create(name="Diesel Estacionario")
    
    def create_greenhouse_gases(self):
        GreenhouseGas.objects.create(name= "CO2")
        GreenhouseGas.objects.create(name= "CH4")
        GreenhouseGas.objects.create(name= "NO2")

    def create_emission_factors(self):
        coloombia_contry = Country.objects.get(name="Colombia")
        co2_greenhouse_gas = GreenhouseGas.objects.get(name="CO2")
        ch4_greenhouse_gas = GreenhouseGas.objects.get(name="CH4")
        no2_greenhouse_gas = GreenhouseGas.objects.get(name="NO2")
        
        diesel_mobile = EmissionSource.objects.get(name="Diesel Movil")
        diesel_stationary = EmissionSource.objects.get(name="Diesel Estacionario")

        EmissionFactor.objects.create(
            value = 0.203,
            country = coloombia_contry,
            greenhouse_gas = co2_greenhouse_gas,
            unit_measurement = UnitMeasurement.objects.get(unit="kg CO2/kWh"),
            emission_source = EmissionSource.objects.get(name="Electricidad")
        )

        EmissionFactor.objects.create(
            value = 10.277,
            country = coloombia_contry,
            greenhouse_gas = co2_greenhouse_gas,
            unit_measurement = UnitMeasurement.objects.get(unit="kg CO2/gal"),
            emission_source = diesel_mobile
        )   

        EmissionFactor.objects.create(
            value = 0.000037,
            country = coloombia_contry,
            greenhouse_gas = ch4_greenhouse_gas,
            unit_measurement = UnitMeasurement.objects.get(unit="kg CH4/gal"),
            emission_source = diesel_mobile
        )   

        EmissionFactor.objects.create(
            value = 0.000037,
            country = coloombia_contry,
            greenhouse_gas = no2_greenhouse_gas,
            unit_measurement = UnitMeasurement.objects.get(unit="kg NO2/gal"),
            emission_source = diesel_mobile
        )   

        EmissionFactor.objects.create(
            value = 10.27,
            country = coloombia_contry,
            greenhouse_gas = co2_greenhouse_gas,
            unit_measurement = UnitMeasurement.objects.get(unit="kg CO2/gal"),
            emission_source = diesel_stationary
        )   

        EmissionFactor.objects.create(
            value = 0.00001,
            country = coloombia_contry,
            greenhouse_gas = ch4_greenhouse_gas,
            unit_measurement = UnitMeasurement.objects.get(unit="kg CH4/gal"),
            emission_source = diesel_stationary
        )   

        EmissionFactor.objects.create(
            value = 0.000006,
            country = coloombia_contry,
            greenhouse_gas = no2_greenhouse_gas,
            unit_measurement = UnitMeasurement.objects.get(unit="kg NO2/gal"),
            emission_source = diesel_stationary
        )  
    

class UnitMeasurementTestCase(AbstractEmissionSourceTestCase):

    def setUp(self):
        self.create_types_unit_measurements()

    def test_create_unit_measurement(self):

        """Create Unit measurements whit typeunits measurements"""
        self.create_units_measurements()
                
        mass_per_energy_measurements = UnitMeasurement.objects.filter(type_unit__name = "Masa por Energia")
        mass_per_gallon_measurements = UnitMeasurement.objects.filter(type_unit__name ="Masa por Galón")

        self.assertEqual(len(mass_per_energy_measurements), 1)
        self.assertEqual(len(mass_per_gallon_measurements), 3)


class EmissionSourceTestCase(AbstractEmissionSourceTestCase):

    def test_create_emission_factor(self):

        """Create Emission Sources"""
        self.create_emission_sources()

        emission_sources  = EmissionSource.objects.all()
        self.assertEqual(len(emission_sources), 3)


class GreenhouseGasTestCase(AbstractEmissionSourceTestCase):

    def test_create_greenhouse_gases(self):
        
        """Create greenhouse geses"""
        self.create_greenhouse_gases()
        greenhosue_gases = GreenhouseGas.objects.all()
        
        self.assertEqual(len(greenhosue_gases), 3)


class EmissionFactorTestCase(AbstractEmissionSourceTestCase):

    def setUp(self):
        Country.objects.create(name="Colombia")
        self.create_types_unit_measurements()
        self.create_units_measurements()
        self.create_emission_sources()
        self.create_greenhouse_gases()

    def test_create_emission_factors(self):

        """Create Emission Factors"""
        self.create_emission_factors()
        
        emission_factors = EmissionFactor.objects.all()

        self.assertEqual(len(emission_factors), 7)


    def test_modify_emission_factors(self):
        
        """Modify Emission Factors"""
        self.create_emission_factors()
        
        electric_emission_factor = EmissionFactor.objects.get(
            greenhouse_gas = GreenhouseGas.objects.get(name="CO2"),
            emission_source = EmissionSource.objects.get(name="Electricidad")
        )

        electric_emission_factor.value = 10.3
        electric_emission_factor.save()

        last_emission_factor_history = HistoryEmissionFactor.objects.last()

        self.assertEqual(last_emission_factor_history.value, electric_emission_factor.value)
        self.assertEqual(last_emission_factor_history.created_at, electric_emission_factor.updated_at)
