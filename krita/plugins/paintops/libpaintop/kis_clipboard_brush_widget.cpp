/*
 *  Copyright (c) 2005 Bart Coppens <kde@bartcoppens.be>
 *  Copyright (c) 2010 Lukáš Tvrdý <lukast.dev@gmail.com>
 *  Copyright (c) 2013 Somsubhra Bairi <somsubhra.bairi@gmail.com>
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

#include "kis_clipboard_brush_widget.h"

#include <QLabel>
#include <QImage>
#include <QPixmap>
#include <QShowEvent>

#include <kglobal.h>
#include <kstandarddirs.h>

#include <KoProperties.h>

#include <kis_debug.h>
#include "kis_image.h"
#include "kis_clipboard.h"
#include "kis_paint_device.h"
#include "kis_gbr_brush.h"
#include "kis_brush_server.h"

KisClipboardBrushWidget::KisClipboardBrushWidget(QWidget *parent, const QString &caption, KisImageWSP image)
    : KisWdgClipboardBrush(parent), m_image(image)
{
    setWindowTitle(caption);
    preview->setScaledContents(true);
    preview->setFixedSize(preview->size());

    KisBrushResourceServer* rServer = KisBrushServer::instance()->brushServer();
    m_rServerAdapter = QSharedPointer<KisBrushResourceServerAdapter>(new KisBrushResourceServerAdapter(rServer));

    m_brush = 0;
    m_brushCreated = false;

    m_clipboard = KisClipboard::instance();

    connect(m_clipboard, SIGNAL(clipChanged()), this, SLOT(slotUseBrushClicked()));
    connect(colorAsmask, SIGNAL(toggled(bool)), this, SLOT(slotUpdateUseColorAsMask(bool)));
    connect(saveBrush, SIGNAL(clicked()), this, SLOT(slotSaveBrush()));

    spacingWidget->setSpacing(true, 1.0);
    connect(spacingWidget, SIGNAL(sigSpacingChanged()), SLOT(slotSpacingChanged()));

    connect(chkSmoothBrush, SIGNAL(toggled(bool)), SLOT(slotUseBrushClicked()));
}

KisClipboardBrushWidget::~KisClipboardBrushWidget()
{
}

KisBrushSP KisClipboardBrushWidget::brush()
{
    return m_brush;
}

void KisClipboardBrushWidget::slotUseBrushClicked()
{

    if (m_clipboard->hasClip()) {

        if (m_brush) {
            bool removedCorrectly = KisBrushServer::instance()->brushServer()->removeResourceFromServer(m_brush.data());

            if (!removedCorrectly) {
                kWarning() << "Brush was not removed correctly from the resource server";
            }
        }

        pd = m_clipboard->clip(QRect(0, 0, 0, 0), false);     //Weird! Don't know how this works!
        if (pd) {
            QRect rc = pd->exactBounds();

            if (chkSmoothBrush->isChecked()) {
                rc = kisGrowRect(rc, 1);
            }

            m_brush = new KisGbrBrush(pd, rc.x(), rc.y(), rc.width(), rc.height());

            m_brush->setSpacing(spacingWidget->spacing());
            m_brush->setAutoSpacing(spacingWidget->autoSpacingActive(), spacingWidget->autoSpacingCoeff());
            m_brush->setFilename(TEMPORARY_CLIPBOARD_BRUSH_FILENAME);
            m_brush->setName(TEMPORARY_CLIPBOARD_BRUSH_NAME);
            m_brush->setValid(true);

            KisBrushServer::instance()->brushServer()->addResource(m_brush.data(), false);

            preview->setPixmap(QPixmap::fromImage(m_brush->image()));

            emit sigBrushChanged();
        }
    }
    else {
        preview->setText("No clip.");
    }
}

void KisClipboardBrushWidget::slotSpacingChanged()
{
    if (m_brush) {
        m_brush->setSpacing(spacingWidget->spacing());
        m_brush->setAutoSpacing(spacingWidget->autoSpacingActive(), spacingWidget->autoSpacingCoeff());
    }
    emit sigBrushChanged();
}

void KisClipboardBrushWidget::showEvent(QShowEvent *)
{
    if (!m_brushCreated) {
        this->slotUseBrushClicked();
        m_brushCreated = true;
    }
}

void KisClipboardBrushWidget::slotUpdateUseColorAsMask(bool useColorAsMask)
{
    if (m_brush) {
        static_cast<KisGbrBrush*>(m_brush.data())->setUseColorAsMask(useColorAsMask);
        preview->setPixmap(QPixmap::fromImage(m_brush->image()));
    }

    emit sigBrushChanged();
}

void KisClipboardBrushWidget::slotSaveBrush()
{
    QString dir = KGlobal::dirs()->saveLocation("data", "krita/brushes");
    QString extension = ".gbr";
    QString name = nameEdit->text();

    QString tempFileName;
    QFileInfo fileInfo;
    fileInfo.setFile(dir + name + extension);

    int i = 1;
    while (fileInfo.exists()) {
        fileInfo.setFile(dir + name + QString("%1").arg(i) + extension);
        i++;
    }
    tempFileName = fileInfo.filePath();

    if (m_rServerAdapter) {
        KisGbrBrush* resource = static_cast<KisGbrBrush*>(m_brush.data())->clone();
        resource->setFilename(tempFileName);

        if (nameEdit->text().isEmpty()) {
            resource->setName(QDateTime::currentDateTime().toString("yyyy-MM-ddThh:mm"));
        }
        else {
            resource->setName(name);
        }

        if (colorAsmask->isChecked()) {
            resource->makeMaskImage();
        }
        m_rServerAdapter->addResource(resource);
    }
}
