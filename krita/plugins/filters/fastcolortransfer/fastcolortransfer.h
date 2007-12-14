/*
 * This file is part of Krita
 *
 * Copyright (c) 2006 Cyrille Berger <cberger@cberger.net>
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
 */

#ifndef COLORTRANSFER_H
#define COLORTRANSFER_H

#include <kparts/plugin.h>
#include <kis_filter.h>

class FastColorTransferPlugin : public KParts::Plugin
{
public:
    FastColorTransferPlugin(QObject *parent, const QStringList &);
    virtual ~FastColorTransferPlugin();
};

class KisFilterFastColorTransfer : public KisFilter
{
public:
    KisFilterFastColorTransfer();
public:
    using KisFilter::process;
    void process(KisFilterConstProcessingInformation src,
                 KisFilterProcessingInformation dst,
                 const QSize& size,
                 const KisFilterConfiguration* config,
                 KoUpdater* progressUpdater
        ) const;
    static inline KoID id() { return KoID("colortransfer", i18n("Color Transfer")); }

public:
    virtual KisFilterConfigWidget * createConfigurationWidget(QWidget* parent, const KisPaintDeviceSP dev);
    virtual KisFilterConfiguration* factoryConfiguration(const KisPaintDeviceSP) const;
};

#endif
