# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'emailNEFT.name'
        db.add_column(u'signup_emailneft', 'name',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'emailNEFT.name'
        db.delete_column(u'signup_emailneft', 'name')


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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
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
            'verification_amount': ('django.db.models.fields.DecimalField', [], {'default': '1.863146808508832', 'max_digits': '5', 'decimal_places': '2'})
        }
    }

    complete_apps = ['signup']