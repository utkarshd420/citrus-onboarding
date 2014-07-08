# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BankChoice'
        db.create_table(u'bank_approvals_bankchoice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bank', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signup.Bank'])),
            ('merchant_name', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('merchant_friendly_name', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('merchant_url', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('merchant_region', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('merchant_category', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('merchant_commercial', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('merchant_type', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('bank_share', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('expected_no_txn', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('expected_no_vol', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('requested_date', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('remarks', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('bank_code', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('merchant_address', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'bank_approvals', ['BankChoice'])

        # Adding model 'receive_mail_banks'
        db.create_table(u'bank_approvals_receive_mail_banks', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bank', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signup.Bank'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='NR', max_length=2, db_index=True)),
            ('file_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('date_changed_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 7, 4, 0, 0))),
        ))
        db.send_create_signal(u'bank_approvals', ['receive_mail_banks'])


    def backwards(self, orm):
        # Deleting model 'BankChoice'
        db.delete_table(u'bank_approvals_bankchoice')

        # Deleting model 'receive_mail_banks'
        db.delete_table(u'bank_approvals_receive_mail_banks')


    models = {
        u'bank_approvals.bankchoice': {
            'Meta': {'object_name': 'BankChoice'},
            'bank': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['signup.Bank']"}),
            'bank_code': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'bank_share': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'expected_no_txn': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'expected_no_vol': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'merchant_address': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'merchant_category': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'merchant_commercial': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'merchant_friendly_name': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'merchant_name': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'merchant_region': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'merchant_type': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'merchant_url': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'remarks': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'requested_date': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'bank_approvals.receive_mail_banks': {
            'Meta': {'object_name': 'receive_mail_banks'},
            'bank': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['signup.Bank']"}),
            'date_changed_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 7, 4, 0, 0)'}),
            'file_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'NR'", 'max_length': '2', 'db_index': 'True'})
        },
        u'signup.bank': {
            'Meta': {'object_name': 'Bank'},
            'bank': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['bank_approvals']