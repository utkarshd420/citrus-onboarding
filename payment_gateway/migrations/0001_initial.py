# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'pg_Bank'
        db.create_table(u'payment_gateway_pg_bank', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bank', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal(u'payment_gateway', ['pg_Bank'])

        # Adding model 'pg_Choice'
        db.create_table(u'payment_gateway_pg_choice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pg_Choice', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'payment_gateway', ['pg_Choice'])

        # Adding model 'pg_BankChoice'
        db.create_table(u'payment_gateway_pg_bankchoice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bank', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['payment_gateway.pg_Bank'])),
            ('choice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['payment_gateway.pg_Choice'])),
            ('include', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'payment_gateway', ['pg_BankChoice'])

        # Adding model 'PaymentMode'
        db.create_table(u'payment_gateway_paymentmode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mode', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'payment_gateway', ['PaymentMode'])

        # Adding model 'CardScheme'
        db.create_table(u'payment_gateway_cardscheme', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('scheme', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'payment_gateway', ['CardScheme'])


    def backwards(self, orm):
        # Deleting model 'pg_Bank'
        db.delete_table(u'payment_gateway_pg_bank')

        # Deleting model 'pg_Choice'
        db.delete_table(u'payment_gateway_pg_choice')

        # Deleting model 'pg_BankChoice'
        db.delete_table(u'payment_gateway_pg_bankchoice')

        # Deleting model 'PaymentMode'
        db.delete_table(u'payment_gateway_paymentmode')

        # Deleting model 'CardScheme'
        db.delete_table(u'payment_gateway_cardscheme')


    models = {
        u'payment_gateway.cardscheme': {
            'Meta': {'object_name': 'CardScheme'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scheme': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'payment_gateway.paymentmode': {
            'Meta': {'object_name': 'PaymentMode'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mode': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'payment_gateway.pg_bank': {
            'Meta': {'object_name': 'pg_Bank'},
            'bank': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'payment_gateway.pg_bankchoice': {
            'Meta': {'object_name': 'pg_BankChoice'},
            'bank': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['payment_gateway.pg_Bank']"}),
            'choice': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['payment_gateway.pg_Choice']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'include': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'payment_gateway.pg_choice': {
            'Meta': {'object_name': 'pg_Choice'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pg_Choice': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['payment_gateway']