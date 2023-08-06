# ScrapSE

## Package description

ScrapSE downloads the judgments in the desired format.  

Currently supported platforms: LEGGI D'ITALIA PA.

### Install scrapse
```
pip install scrapse
```

### How to use

#### Saving cookies - important
```
scrapse leggitalia save-cookie 'your_cokies'
```
This command creates a `.txt` file containing `your_cookie`.

#### Show filter values
```
scrapse leggitalia show
```
This command shows the possible values to be assigned to sentence search filters.

#### Download the judgments
Make sure you have **saved** platform-related cookies before downloading the judgments!.
```
scrapse leggitalia scrap -l torino -s 'Sez. lavoro, Sez. V'
```
This command creates a folder in `Users/your_username` named `sez.lavoro&sez.v_torino` containing the judgments.

#### For more help
```
scrapse --help
```
