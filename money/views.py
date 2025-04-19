from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder

from django.http import JsonResponse
import json
from .models import *
from .form import *

def index(request):
    cashes = CashFlow.objects.all()

    # Фильтрация по дате
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")
    if date_from:
        cashes = cashes.filter(date__gte=date_from)
    if date_to:
        cashes = cashes.filter(date__lte=date_to)

    # Фильтрация по статусу, типу, категории, подкатегории
    if status := request.GET.get("status"):
        cashes = cashes.filter(status_id=status)
    if type_ := request.GET.get("type"):
        cashes = cashes.filter(type_id=type_)
    if category := request.GET.get("category"):
        cashes = cashes.filter(category_id=category)
    if subcategory := request.GET.get("subcategory"):
        cashes = cashes.filter(subcategory_id=subcategory)

    # Связи для бизнес-правил
    type_categories = {
        type_.id: list(type_.categories.values_list("id", flat=True))  
        for type_ in Type.objects.all()
    }

    category_subcategories = {
        cat.id: list(cat.subcategories.values_list("id", flat=True))  
        for cat in Category.objects.all()
    }

    relations = {
        "type_categories": type_categories,
        "category_subcategories": category_subcategories,
    }

    context = {
        "cashes": cashes,
        "statuses": Status.objects.all(),
        "types": Type.objects.all(),
        "categories": Category.objects.all(),
        "subcategories": SubCategory.objects.all(),
        "relations_json": json.dumps(relations, cls=DjangoJSONEncoder),  
    }

    return render(request, "money/index.html", context)


# Создание
def create(request):
    if request.method == "POST":
        form = CashFlowForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")  
        else:
            # Форма не прошла валидацию, ошибки будут показаны в шаблоне
            return render(request, "money/create.html", {"cashflow": form})
    else:
        cashflow_form = CashFlowForm()

        categories = list(Category.objects.values("id", "name", "type_id"))
        subcategories = list(SubCategory.objects.values("id", "name", "category_id"))

        context = {
            "cashflow": cashflow_form,
            "categories_json": json.dumps(categories, cls=DjangoJSONEncoder),
            "subcategories_json": json.dumps(subcategories, cls=DjangoJSONEncoder)
        }
        return render(request, "money/create.html", context)

# Контроль справочников
def control(request):
    if request.method == "POST":
    
        
        # в конце каждой формы есть hidden input у которого имя это тип формы     
        which_form = request.POST.get("form_type")

        # Валидность и сохранение
        if which_form == "status":
            status_form = StatusForm(request.POST)
            if status_form.is_valid():
                status_form.save()
            else:
                status_form = StatusForm()

        if which_form == "type":
            type_form = TypeForm(request.POST)
            if type_form.is_valid():
                type_form.save()
            else:
                type_form = TypeForm()

        if which_form == "category":
            category_form = CategoryForm(request.POST)
            if category_form.is_valid():
                category_form.save()
            else:
                category_form = CategoryForm()

        if which_form == "subcategory":
            subcategory_form = SubcategoryForm(request.POST)
            if subcategory_form.is_valid():
                subcategory_form.save()
            else:
                subcategory_form = SubcategoryForm()

        return redirect("control")
    
    else:
        # Все формы
        type_form =TypeForm()
        category_form = CategoryForm()
        subcategory_form = SubcategoryForm()
        status_form = StatusForm()

    # Все элементы в обратном порядке, чтобы последнее созданное было наверху
    types =Type.objects.all().order_by("-id")
    categories = Category.objects.all().order_by("-id")
    subcategories = SubCategory.objects.all().order_by("-id")
    statuses = Status.objects.all().order_by("-id")

    context = {
        "type_f":type_form,
        "category_f":category_form,
        "subcategory_f":subcategory_form,
        "status_f": status_form,

        "types":types,
        "statuses":statuses,
        "categories":categories,
        "subcategories":subcategories
    }
    return render(request, "money/control.html", context)

# Удаление элементов со спрвочников
@csrf_exempt
def delete_item(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            item_type = data.get("item_type")
            item_id = data.get("item_id")

            match item_type:
                case "status":
                    Status.objects.filter(pk=item_id).delete()
                case "type":
                    Type.objects.filter(pk=item_id).delete()
                case "category":
                    Category.objects.filter(pk=item_id).delete()
                case "subcategory":
                    SubCategory.objects.filter(pk=item_id).delete()
                case _:
                    return JsonResponse({"error": "Неправильный тип"}, status=400)

            return JsonResponse({"success": True})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Неправильный метод"}, status=405)


def edit(request, num):
    cash = get_object_or_404(CashFlow, id=num)

    if request.method == "POST":
        form = CashFlowForm(request.POST, instance=cash)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = CashFlowForm(instance=cash)

    categories = list(Category.objects.values("id", "name", "type_id"))
    subcategories = list(SubCategory.objects.values("id", "name", "category_id"))

    context = {
        "cashflow": form,
        "categories_json": json.dumps(categories, cls=DjangoJSONEncoder),
        "subcategories_json": json.dumps(subcategories, cls=DjangoJSONEncoder),
        "is_edit": True,  # чтобы в шаблоне можно было отличить создание от редактирования
        "edit_id": cash.id,  # для возможных ссылок или скрытого поля
    }

    return render(request, "money/create.html", context)


# Удаление записи из таблицы
@csrf_exempt
def delete_cashflow(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            cash_id = data.get("cashflow_id")
            CashFlow.objects.filter(id=cash_id).delete()
            return JsonResponse({"ok":True})
        except Exception as ex:
            return JsonResponse({"error":"Неверный метод"})
        