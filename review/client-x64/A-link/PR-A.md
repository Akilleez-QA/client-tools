# Remove unused explicit Win32 Release link inputs

The SwgClient Release project lists libraries that its link does not use. This change removes 74 explicit entries while preserving the tested product link output after the documented timestamp/PDB-age normalization.

Scope: one XML line replaced (+1/-1), based on upstream `94945103`. Release is the only configuration changed and validated. Debug and Optimized remain unchanged because their library use has not been independently proven; extending the cleanup requires a separate proof for each configuration.

## Validation

See [RESULTS.md](https://github.com/Akilleez-QA/client-tools/blob/review/client-x64-evidence/review/client-x64/A-link/RESULTS.md) for the exact branch/base, native product build and comparison result. These findings apply to explicit link inputs; they do not establish absence of dynamically loaded dependencies or source-level default-library directives.

## Removed entries

Case-distinct duplicate spellings are retained in this list exactly as removed from the project:

### Maya (11)

`Foundation.lib`, `Image.lib`, `libMDtAPI.lib`, `libMocap.lib`, `OpenMaya.lib`, `OpenMayaAnim.lib`, `OpenMayaFX.lib`, `OpenMayaRender.lib`, `OpenMayaUI.lib`, `libMDtApi.lib`, `libmocap.lib`.

### Cg / Cloth / image / OpenEXR / FBX (9)

`cg.lib`, `cgGL.lib`, `Cloth.lib`, `IMF.lib`, `libfbxfilesdk.lib`, `libHalf.lib`, `libIex.lib`, `libIlmImf.lib`, `libImath.lib`.

### Alienbrain (3)

`libclient.lib`, `librpc.lib`, `libsupp.lib`.

### Qt / Qt tools and plugins (51)

`designercore.lib`, `editor.lib`, `qassistantclient.lib`, `qaxcontainer.lib`, `qt-mt334.lib`, `qtmain.lib`, `qui.lib`, `qtwidgets100.lib`, `cppeditor100.lib`, `dlgplugin.lib`, `gladeplugin.lib`, `kdevdlgplugin.lib`, `qaxwidget100.lib`, `rcplugin.lib`, `wizards.lib`, `qjpeg100.lib`, `qmng100.lib`, `QAxContainerd.lib`, `Qt3Supportd4.lib`, `QtAssistantClientd.lib`, `QtCored4.lib`, `QtDesignerComponentsd4.lib`, `QtDesignerd4.lib`, `QtGuid4.lib`, `qtmaind.lib`, `QtNetworkd4.lib`, `QtOpenGLd4.lib`, `QtSqld4.lib`, `QtSvgd4.lib`, `QtTest_debug4.lib`, `QtUiTools.lib`, `QtXmld4.lib`, `qtaccessiblecompatwidgetsd1.lib`, `qtaccessiblewidgetsd1.lib`, `qcncodecsd.lib`, `qjpcodecsd.lib`, `qkrcodecsd.lib`, `qtwcodecsd.lib`, `arthurplugin.lib`, `containerextension.lib`, `customwidgetplugin.lib`, `qaxwidget.lib`, `qt3supportwidgets.lib`, `taskmenuextension.lib`, `worldtimeclockplugin.lib`, `qjpegd1.lib`, `qmngd1.lib`, `qsqlited.lib`, `qsqlmysqld.lib`, `qsqlodbcd.lib`, `qsqlpsqld.lib`.
