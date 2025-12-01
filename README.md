# EasyDA

Локальное приложение для быстрого анализа CSV данных.

## Установка

```bash
git clone https://github.com/arthuraswork/easyda
cd easyda
make run
```

## Функционал

### Data Loading
- **Upload CSV** - загрузка файла через file uploader
- **File validation** - проверка размера файла (до 200MB)
- **Data preview** - автоматический просмотр загруженной таблицы

### Data Selection
- **Column selection** - выбор колонки через radio buttons
- **Auto-detect data type** - автоматическое определение типа данных

### Statistical Analysis
- **Metric calculation** - вычисление выбранной метрики кнопкой "Calculate"
- **Numerical data metrics:**
  - mean, median, min, max, mode
  - std, var, skew, kurt, sum
  - describe, sort (ascending/descending)
- **Text data metrics:**
  - values, values-normalize, unique
  - isna, duplicated
- **Mode count adjustment** - настройка количества мод через слайдер

### Visualization
- **Plot generation** - построение графиков кнопкой "Plot"
- **Plot type selection** - выбор типа графика (hist/area) через pills
- **Auto-chart type** - автоматический выбор типа графика по типу данных

### Data Operations
- **Custom queries** - выполнение pandas query через текстовое поле + кнопка "Request"
- **Data reset** - возврат к исходным данным кнопкой "Reset"
- **Real-time updates** - автоматическое обновление интерфейса после действий

### Settings
- **Mode count** - настройка количества отображаемых мод
- **Plot type** - выбор типа визуализации