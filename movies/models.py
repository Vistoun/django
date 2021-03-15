from django.db import models
# Import metod MaxValueValidator, MinValueValidator z balíku django.core.validators
from django.core.validators import MaxValueValidator, MinValueValidator
# Import metody reverse z balíku django.urls - zajistí generování URL obrácením URL patterns
from django.urls import reverse


""" Metoda vrací cestu k uploadovaným souborů - přílohám filmů.
 Cesta má obecnou podobu: film/id-filmu/attachments/nazev-souboru. 
 Parametr instance odkazuje na instanci (objekt) filmu.
 Parametr filename obsahuje název uploadovaného souboru. """

def attachment_path(instance, filename):
    return "film/" + str(instance.film.id) + "/attachments/" + filename

""" Metoda vrací cestu k uploadovanému plakátu. """
def poster_path(instance, filename):
 return "film/" + str(instance.id) + "/poster/" + filename

""" Třída Genre je modelem pro databázový objekt (tabulku), v němž budou ukládány názvy 
žánrů filmů
V závorce za názvem třídy je uvedena třída-předek Model pocházející z knihovny (balíku, 
modulu) models (models.Model)
Je zde využit princip dědičnosti - všechny naše vlastní modely pocházejí ze společného 
předka třídy Model
a dědí její vlastnosti """
class Genre(models.Model):

    """Fields - definice jednotlivých polí/sloupců modelu/tabulky
    Každé pole modelu (budoucí tabulky v databázi) je uloženo do vhodně pojmenované 
    proměnné/atributu - zde "name"
    Vzniká jako instance určité třídy (zde models.CharField), která rozhoduje o datovém 
    typu pole a o jeho vlastnostech
    V tomto případě bude pole "name" obsahovat maximálně 50 znaků (parametr max_length),
    bude obsahovat unikátní hodnoty (parametr unique),
    ve formuláři se bude zobrazovat pod označením "Genre name" (parametr verbose_name),
    a uživateli se jako nápověda nabídne text uvedený v parametru help_text """

    name = models.CharField(max_length=50, unique=True, verbose_name="Genre name", help_text='Enter a film genre (e.g. sci-fi, comedy)')

    """ Metadata - slouží ke specifikaci některých dalších vlastností modelu, jež ale už 
    mohou být v řadě případů závislé i na konkrétním typu použité databáze """

    class Meta:
        # atribut ordering definuje upřednostňovaný způsob řazení - zde vzestupně podle pole/sloupce name
        ordering = ["name"]

        """ Methods - definují chování objektu v určité situaci """
    def __str__(self):
        """ Řetězec, který se používá jako textová reprezentace objektu (například v 
            administraci aplikace).
            V našem případě bude objekt (žánr) reprezentován výpisem obsahu pole name """
        return self.name


    """ Třída Film je modelem pro databázový objekt (tabulku), který bude obsahovat základní 
    údaje o filmech """

class Film(models.Model):
    # Fields
    # Znakové pole o maximální délce 200 znaků pro vložení názvu filmu
    title = models.CharField(max_length=200, verbose_name="Title")

    # Textové pole pro vložení delšího textu popisujícího děj filmu
    # Formulářový prvek může zůstat prázdný - parametry blank=True, null=True
    plot = models.TextField(blank=True, null=True, verbose_name="Plot")
    # Pole obsahuje datum uvedení filmu, které musí být zadáno v náležitém tvaru (YYYY-MMDD); nepovinný údaj
    release_date = models.DateField(blank=True, null=True, help_text="Please use the following format: <em>YYYY-MM-DD</em>.", verbose_name="Release date")
    # Celočíselné pole pro nepovinné zadání stopáže (délky) filmu v minutách
    runtime = models.IntegerField(blank=True, null=True, help_text="Please enter an integer value (minutes)", verbose_name="Runtime")
    # Pole pro zadání desetinného čísla vyjadřujícího hodnocení filmu v rozsahu 1.0 až 10.0
    # Výchozí hodnota je nastavena na 5.0
    # K validaci hodnot jsou použity metody z balíku/knihovny django.core.validators
    rate = models.FloatField(default=5.0, validators=[MinValueValidator(1.0), MaxValueValidator(10.0)], null=True, help_text="Please enter an float value (range 1.0 - 10.0)",verbose_name="Rate")
    # Vytvoří vztah mezi modely Film a Genre typu M:N
    genres = models.ManyToManyField(Genre, help_text='Select a genre for this film')
    # Pole typu image, které umožňuje upload obrázku s plakátem filmu
    poster = models.ImageField(upload_to=poster_path, blank=True, null=True, verbose_name="Poster")

    # Metadata
    class Meta:
        # Záznamy budou řazeny primárně sestupně (znaménko mínus) podle data uvedení,
        # sekundárně vzestupně podle názvu
        ordering = ["-release_date", "title"]
        # Methods
    def __str__(self):
        """Součástí textové reprezentace filmu bude jeho název, rok uvedení a hodnocení"""
        return f"{self.title}, year: {str(self.release_date.year)}, rate: {str(self.rate)}"

    def get_absolute_url(self):
        """Metoda vrací URL stránky, na které se vypisují podrobné informace o filmu"""
        return reverse('film-detail', args=[str(self.id)])


""" Třída Attachment je modelem pro databázový objekt (tabulku), který bude obsahovat 
údaje o přílohách filmů """

class Attachment(models.Model):
    # Fields
    # Povinný titulek přílohy - text do délky 200 znaků
    title = models.CharField(max_length=200, verbose_name="Title")
    # Časový údaj o poslední aktualizaci přílohy - automaticky se ukládá aktuální čas
    last_update = models.DateTimeField(auto_now=True)
    # Pole pro upload souboru
    # Parametr upload_to zajistí uložení souboru do složky specifikované v návratové  hodnotě metody attachment_path
    file = models.FileField(upload_to=attachment_path, null=True, verbose_name="File")
    # Konstanta, v níž jsou ve formě n-tic (tuples) předdefinovány různé typy příloh
    TYPE_OF_ATTACHMENT = (
        ('audio', 'Audio'),
        ('image', 'Image'),
        ('text', 'Text'),
        ('video', 'Video'),
        ('other', 'Other'),
    )
    # Pole s definovanými předvolbami pro uložení typu přílohy
    type = models.CharField(max_length=5, choices=TYPE_OF_ATTACHMENT, blank=True, default='image', help_text='Select allowed attachment type', verbose_name="Attachment type")
    # Cizí klíč, který zajišťuje propojení přílohy s daným filmem (vztah N:1)
    # Parametr on_delete slouží k zajištění tzv. referenční integrity - v případě odstranění filmu
    # budou odstraněny i všechny jeho přílohy (models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)

    # Metadata
    class Meta:
        # Primární seřazeno podle poslední aktualizace souborů, sekundárně podle typu přílohy
        ordering = ["-last_update", "type"]

    # Methods
    def __str__(self):
        """ Textová reprezentace objektu """
        return f"{self.title}, ({self.type})"