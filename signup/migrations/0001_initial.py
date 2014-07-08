# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Merchant'
        db.create_table(u'signup_merchant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('step', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('application_status', self.gf('django.db.models.fields.CharField')(default='N', max_length=2, db_index=True)),
            ('last_changed_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 7, 4, 0, 0))),
            ('verified_account', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'signup', ['Merchant'])

        # Adding model 'CompanyCategory'
        db.create_table(u'signup_companycategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('bank_commercial_citrus', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('mode_bank', self.gf('django.db.models.fields.CharField')(default='PERC', max_length=4, db_index=True)),
            ('merchant_commercial_citrus', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('mode_merchant', self.gf('django.db.models.fields.CharField')(default='PERC', max_length=4, db_index=True)),
        ))
        db.send_create_signal(u'signup', ['CompanyCategory'])

        # Adding model 'BusinessType'
        db.create_table(u'signup_businesstype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'signup', ['BusinessType'])

        # Adding model 'Company'
        db.create_table(u'signup_company', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('merchant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signup.Merchant'])),
            ('company_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signup.CompanyCategory'])),
            ('business_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signup.BusinessType'])),
            ('friendly_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'signup', ['Company'])

        # Adding model 'Bank'
        db.create_table(u'signup_bank', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bank', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal(u'signup', ['Bank'])

        # Adding model 'MerchantBankApproval'
        db.create_table(u'signup_merchantbankapproval', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signup.Company'])),
            ('bank', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signup.Bank'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='P', max_length=2, db_index=True)),
            ('remarks', self.gf('django.db.models.fields.CharField')(max_length=320, blank=True)),
            ('date_mailed_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('date_received_status', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('employee_assigned_to', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
        ))
        db.send_create_signal(u'signup', ['MerchantBankApproval'])

        # Adding model 'Service'
        db.create_table(u'signup_service', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('charges', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('included_in_default', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'signup', ['Service'])

        # Adding model 'MerchantService'
        db.create_table(u'signup_merchantservice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('merchant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signup.Merchant'])),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signup.Service'])),
        ))
        db.send_create_signal(u'signup', ['MerchantService'])

        # Adding model 'Txn'
        db.create_table(u'signup_txn', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('merchant_tx_id', self.gf('django.db.models.fields.CharField')(max_length=64, db_index=True)),
            ('merchant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signup.Merchant'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='P', max_length=2, db_index=True)),
            ('citrus_tx_id', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=64, null=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('date_time', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('verification_amount', self.gf('django.db.models.fields.DecimalField')(default=3.5988284691592956, max_digits=5, decimal_places=2)),
        ))
        db.send_create_signal(u'signup', ['Txn'])

        # Adding model 'bank_commercial_value'
        db.create_table(u'signup_bank_commercial_value', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('mode', self.gf('django.db.models.fields.CharField')(default='PERC', max_length=4, db_index=True)),
            ('from_merchant', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('bank_commercial', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signup.bank_commercial'])),
        ))
        db.send_create_signal(u'signup', ['bank_commercial_value'])

        # Adding model 'bank_commercial'
        db.create_table(u'signup_bank_commercial', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bank', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signup.Bank'])),
            ('company_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signup.CompanyCategory'], null=True, blank=True)),
        ))
        db.send_create_signal(u'signup', ['bank_commercial'])

        # Adding model 'commercial'
        db.create_table(u'signup_commercial', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bank', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signup.Bank'])),
            ('commercial_value', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('mode', self.gf('django.db.models.fields.CharField')(default='PERC', max_length=4, db_index=True)),
            ('merchant_commercial', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signup.merchant_commercial'])),
        ))
        db.send_create_signal(u'signup', ['commercial'])

        # Adding model 'merchant_commercial'
        db.create_table(u'signup_merchant_commercial', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signup.Company'])),
        ))
        db.send_create_signal(u'signup', ['merchant_commercial'])

        # Adding model 'document'
        db.create_table(u'signup_document', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('header', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('doc_list', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('businessType', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signup.BusinessType'])),
        ))
        db.send_create_signal(u'signup', ['document'])

        # Adding model 'action_mail'
        db.create_table(u'signup_action_mail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('head', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('limit', self.gf('django.db.models.fields.IntegerField')()),
            ('age', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'signup', ['action_mail'])

        # Adding model 'document_user_status'
        db.create_table(u'signup_document_user_status', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('merchant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signup.Merchant'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('uploaded', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('join_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 7, 4, 0, 0))),
            ('last_reminder', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 7, 4, 0, 0))),
        ))
        db.send_create_signal(u'signup', ['document_user_status'])

        # Adding model 'merchant_address'
        db.create_table(u'signup_merchant_address', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('flat_no', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('building_name', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('street_name', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('road_name', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('area_name', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
        ))
        db.send_create_signal(u'signup', ['merchant_address'])

        # Adding model 'current_pg'
        db.create_table(u'signup_current_pg', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name_pg', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'signup', ['current_pg'])

        # Adding model 'additional_company_details'
        db.create_table(u'signup_additional_company_details', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('merchant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signup.Merchant'])),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signup.merchant_address'])),
            ('date_of_establishment', self.gf('django.db.models.fields.DateTimeField')()),
            ('min_ticket_size', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('max_ticket_size', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('avg_monthly_volume', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('company_turnover', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('current_pg_service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signup.current_pg'], null=True, blank=True)),
            ('international_card_required', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'signup', ['additional_company_details'])

        # Adding model 'merchant_contact'
        db.create_table(u'signup_merchant_contact', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('contact_number', self.gf('django.db.models.fields.IntegerField')(max_length=12)),
        ))
        db.send_create_signal(u'signup', ['merchant_contact'])

        # Adding model 'merchant_contact_details'
        db.create_table(u'signup_merchant_contact_details', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('merchant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signup.Merchant'])),
            ('merchant_business_contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signup.merchant_contact'])),
        ))
        db.send_create_signal(u'signup', ['merchant_contact_details'])

        # Adding model 'merchant_website_details'
        db.create_table(u'signup_merchant_website_details', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('merchant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signup.Merchant'])),
            ('about_us_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('contact_us_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('terms_conditions_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('prduct_description_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('returns_refund_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('privacy_policy_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('shipping_delivery_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('disclaimer_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal(u'signup', ['merchant_website_details'])

        # Adding model 'emailNEFT'
        db.create_table(u'signup_emailneft', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal(u'signup', ['emailNEFT'])


    def backwards(self, orm):
        # Deleting model 'Merchant'
        db.delete_table(u'signup_merchant')

        # Deleting model 'CompanyCategory'
        db.delete_table(u'signup_companycategory')

        # Deleting model 'BusinessType'
        db.delete_table(u'signup_businesstype')

        # Deleting model 'Company'
        db.delete_table(u'signup_company')

        # Deleting model 'Bank'
        db.delete_table(u'signup_bank')

        # Deleting model 'MerchantBankApproval'
        db.delete_table(u'signup_merchantbankapproval')

        # Deleting model 'Service'
        db.delete_table(u'signup_service')

        # Deleting model 'MerchantService'
        db.delete_table(u'signup_merchantservice')

        # Deleting model 'Txn'
        db.delete_table(u'signup_txn')

        # Deleting model 'bank_commercial_value'
        db.delete_table(u'signup_bank_commercial_value')

        # Deleting model 'bank_commercial'
        db.delete_table(u'signup_bank_commercial')

        # Deleting model 'commercial'
        db.delete_table(u'signup_commercial')

        # Deleting model 'merchant_commercial'
        db.delete_table(u'signup_merchant_commercial')

        # Deleting model 'document'
        db.delete_table(u'signup_document')

        # Deleting model 'action_mail'
        db.delete_table(u'signup_action_mail')

        # Deleting model 'document_user_status'
        db.delete_table(u'signup_document_user_status')

        # Deleting model 'merchant_address'
        db.delete_table(u'signup_merchant_address')

        # Deleting model 'current_pg'
        db.delete_table(u'signup_current_pg')

        # Deleting model 'additional_company_details'
        db.delete_table(u'signup_additional_company_details')

        # Deleting model 'merchant_contact'
        db.delete_table(u'signup_merchant_contact')

        # Deleting model 'merchant_contact_details'
        db.delete_table(u'signup_merchant_contact_details')

        # Deleting model 'merchant_website_details'
        db.delete_table(u'signup_merchant_website_details')

        # Deleting model 'emailNEFT'
        db.delete_table(u'signup_emailneft')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'signup.action_mail': {
            'Meta': {'object_name': 'action_mail'},
            'age': ('django.db.models.fields.IntegerField', [], {}),
            'head': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limit': ('django.db.models.fields.IntegerField', [], {})
        },
        u'signup.additional_company_details': {
            'Meta': {'object_name': 'additional_company_details'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['signup.merchant_address']"}),
            'avg_monthly_volume': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'company_turnover': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'current_pg_service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['signup.current_pg']", 'null': 'True', 'blank': 'True'}),
            'date_of_establishment': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'international_card_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'max_ticket_size': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'merchant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['signup.Merchant']"}),
            'min_ticket_size': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        u'signup.bank': {
            'Meta': {'object_name': 'Bank'},
            'bank': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'signup.bank_commercial': {
            'Meta': {'object_name': 'bank_commercial'},
            'bank': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['signup.Bank']"}),
            'company_category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['signup.CompanyCategory']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'signup.bank_commercial_value': {
            'Meta': {'object_name': 'bank_commercial_value'},
            'bank_commercial': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['signup.bank_commercial']"}),
            'from_merchant': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mode': ('django.db.models.fields.CharField', [], {'default': "'PERC'", 'max_length': '4', 'db_index': 'True'}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'})
        },
        u'signup.businesstype': {
            'Meta': {'object_name': 'BusinessType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'signup.commercial': {
            'Meta': {'object_name': 'commercial'},
            'bank': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['signup.Bank']"}),
            'commercial_value': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'merchant_commercial': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['signup.merchant_commercial']"}),
            'mode': ('django.db.models.fields.CharField', [], {'default': "'PERC'", 'max_length': '4', 'db_index': 'True'})
        },
        u'signup.company': {
            'Meta': {'object_name': 'Company'},
            'business_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['signup.BusinessType']"}),
            'company_category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['signup.CompanyCategory']"}),
            'friendly_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'merchant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['signup.Merchant']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'signup.companycategory': {
            'Meta': {'object_name': 'CompanyCategory'},
            'bank_commercial_citrus': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'merchant_commercial_citrus': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'mode_bank': ('django.db.models.fields.CharField', [], {'default': "'PERC'", 'max_length': '4', 'db_index': 'True'}),
            'mode_merchant': ('django.db.models.fields.CharField', [], {'default': "'PERC'", 'max_length': '4', 'db_index': 'True'})
        },
        u'signup.current_pg': {
            'Meta': {'object_name': 'current_pg'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_pg': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'signup.document': {
            'Meta': {'object_name': 'document'},
            'businessType': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['signup.BusinessType']"}),
            'doc_list': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'header': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'signup.document_user_status': {
            'Meta': {'object_name': 'document_user_status'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'join_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 7, 4, 0, 0)'}),
            'last_reminder': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 7, 4, 0, 0)'}),
            'merchant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['signup.Merchant']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'uploaded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'signup.emailneft': {
            'Meta': {'object_name': 'emailNEFT'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'signup.merchant': {
            'Meta': {'object_name': 'Merchant'},
            'application_status': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '2', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_changed_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 7, 4, 0, 0)'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'step': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'verified_account': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'signup.merchant_address': {
            'Meta': {'object_name': 'merchant_address'},
            'area_name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'building_name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'flat_no': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'road_name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'street_name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'})
        },
        u'signup.merchant_commercial': {
            'Meta': {'object_name': 'merchant_commercial'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['signup.Company']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'signup.merchant_contact': {
            'Meta': {'object_name': 'merchant_contact'},
            'contact_number': ('django.db.models.fields.IntegerField', [], {'max_length': '12'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'signup.merchant_contact_details': {
            'Meta': {'object_name': 'merchant_contact_details'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'merchant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['signup.Merchant']"}),
            'merchant_business_contact': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['signup.merchant_contact']"})
        },
        u'signup.merchant_website_details': {
            'Meta': {'object_name': 'merchant_website_details'},
            'about_us_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'contact_us_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'disclaimer_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'merchant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['signup.Merchant']"}),
            'prduct_description_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'privacy_policy_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'returns_refund_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'shipping_delivery_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'terms_conditions_url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'signup.merchantbankapproval': {
            'Meta': {'object_name': 'MerchantBankApproval'},
            'bank': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['signup.Bank']"}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['signup.Company']"}),
            'date_mailed_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_received_status': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'employee_assigned_to': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remarks': ('django.db.models.fields.CharField', [], {'max_length': '320', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '2', 'db_index': 'True'})
        },
        u'signup.merchantservice': {
            'Meta': {'object_name': 'MerchantService'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'merchant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['signup.Merchant']"}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['signup.Service']"})
        },
        u'signup.service': {
            'Meta': {'object_name': 'Service'},
            'charges': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'included_in_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'signup.txn': {
            'Meta': {'object_name': 'Txn'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'citrus_tx_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'date_time': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'merchant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['signup.Merchant']"}),
            'merchant_tx_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '2', 'db_index': 'True'}),
            'verification_amount': ('django.db.models.fields.DecimalField', [], {'default': '3.5988284691592956', 'max_digits': '5', 'decimal_places': '2'})
        }
    }

    complete_apps = ['signup']