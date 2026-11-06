from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):
    dependencies = [('store', '0002_purchase_purchase_date')]

    operations = [
        migrations.AlterField(
            model_name='purchase', name='quantity',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AddConstraint(
            model_name='purchase',
            constraint=models.CheckConstraint(
                check=models.Q(quantity__gte=1), name='purchase_quantity_positive',
            ),
        ),
    ]
