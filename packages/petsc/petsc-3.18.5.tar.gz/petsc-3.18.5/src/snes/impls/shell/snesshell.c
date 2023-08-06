#include <petsc/private/snesimpl.h> /*I   "petscsnes.h"   I*/

typedef struct {
  PetscErrorCode (*solve)(SNES, Vec);
  void *ctx;
} SNES_Shell;

/*@C
   SNESShellSetSolve - Sets routine to apply as solver

   Logically Collective

   Input Parameters:
+  snes - the `SNES` nonlinear solver context
-  apply - the application-provided solver routine

   Calling sequence of solve:
.vb
   PetscErrorCode apply (SNES snes,Vec xout)
.ve

+  snes - the preconditioner, get the application context with `SNESShellGetContext()` provided with `SNESShelletContext()`
-  xout - solution vector

   Level: advanced

.seealso: `SNESSHELL`, `SNESShellSetContext()`, `SNESShellGetContext()`
@*/
PetscErrorCode SNESShellSetSolve(SNES snes, PetscErrorCode (*solve)(SNES, Vec))
{
  PetscFunctionBegin;
  PetscValidHeaderSpecific(snes, SNES_CLASSID, 1);
  PetscTryMethod(snes, "SNESShellSetSolve_C", (SNES, PetscErrorCode(*)(SNES, Vec)), (snes, solve));
  PetscFunctionReturn(0);
}

PetscErrorCode SNESReset_Shell(SNES snes)
{
  PetscFunctionBegin;
  PetscFunctionReturn(0);
}

PetscErrorCode SNESDestroy_Shell(SNES snes)
{
  PetscFunctionBegin;
  PetscCall(SNESReset_Shell(snes));
  PetscCall(PetscFree(snes->data));
  PetscFunctionReturn(0);
}

PetscErrorCode SNESSetUp_Shell(SNES snes)
{
  PetscFunctionBegin;
  PetscFunctionReturn(0);
}

PetscErrorCode SNESSetFromOptions_Shell(SNES snes, PetscOptionItems *PetscOptionsObject)
{
  PetscFunctionBegin;
  PetscOptionsHeadBegin(PetscOptionsObject, "SNES Shell options");
  PetscFunctionReturn(0);
}

PetscErrorCode SNESView_Shell(SNES snes, PetscViewer viewer)
{
  PetscFunctionBegin;
  PetscFunctionReturn(0);
}

/*@
    SNESShellGetContext - Returns the user-provided context associated with a `SNESSHELL`

    Not Collective

    Input Parameter:
.   snes - should have been created with `SNESSetType`(snes,`SNESSHELL`);

    Output Parameter:
.   ctx - the user provided context

    Level: advanced

.seealso: `SNESSHELL`, `SNESCreateShell()`, `SNESShellSetContext()`
@*/
PetscErrorCode SNESShellGetContext(SNES snes, void *ctx)
{
  PetscBool flg;

  PetscFunctionBegin;
  PetscValidHeaderSpecific(snes, SNES_CLASSID, 1);
  PetscValidPointer(ctx, 2);
  PetscCall(PetscObjectTypeCompare((PetscObject)snes, SNESSHELL, &flg));
  if (!flg) *(void **)ctx = NULL;
  else *(void **)ctx = ((SNES_Shell *)(snes->data))->ctx;
  PetscFunctionReturn(0);
}

/*@
    SNESShellSetContext - sets the context for a `SNESSHELL`

   Logically Collective

    Input Parameters:
+   snes - the `SNESSHELL`
-   ctx - the context

   Level: advanced

   Fortran Note:
   The context can only be an integer or a `PetscObject` it cannot be a Fortran array or derived type.

.seealso: `SNESSHELL`, `SNESCreateShell()`, `SNESShellGetContext()`
@*/
PetscErrorCode SNESShellSetContext(SNES snes, void *ctx)
{
  SNES_Shell *shell = (SNES_Shell *)snes->data;
  PetscBool   flg;

  PetscFunctionBegin;
  PetscValidHeaderSpecific(snes, SNES_CLASSID, 1);
  PetscCall(PetscObjectTypeCompare((PetscObject)snes, SNESSHELL, &flg));
  if (flg) shell->ctx = ctx;
  PetscFunctionReturn(0);
}

PetscErrorCode SNESSolve_Shell(SNES snes)
{
  SNES_Shell *shell = (SNES_Shell *)snes->data;

  PetscFunctionBegin;
  PetscCheck(shell->solve, PetscObjectComm((PetscObject)snes), PETSC_ERR_ARG_WRONGSTATE, "Must call SNESShellSetSolve() first");
  snes->reason = SNES_CONVERGED_ITS;
  PetscCall((*shell->solve)(snes, snes->vec_sol));
  PetscFunctionReturn(0);
}

PetscErrorCode SNESShellSetSolve_Shell(SNES snes, PetscErrorCode (*solve)(SNES, Vec))
{
  SNES_Shell *shell = (SNES_Shell *)snes->data;

  PetscFunctionBegin;
  shell->solve = solve;
  PetscFunctionReturn(0);
}

/*MC
  SNESSHELL - a user provided nonlinear solver

   Level: advanced

.seealso: `SNESCreate()`, `SNES`, `SNESSetType()`, `SNESType`, `SNESShellGetContext()`, `SNESShellSetContext()`, `SNESShellSetSolve()`
M*/

PETSC_EXTERN PetscErrorCode SNESCreate_Shell(SNES snes)
{
  SNES_Shell *shell;

  PetscFunctionBegin;
  snes->ops->destroy        = SNESDestroy_Shell;
  snes->ops->setup          = SNESSetUp_Shell;
  snes->ops->setfromoptions = SNESSetFromOptions_Shell;
  snes->ops->view           = SNESView_Shell;
  snes->ops->solve          = SNESSolve_Shell;
  snes->ops->reset          = SNESReset_Shell;

  snes->usesksp = PETSC_FALSE;
  snes->usesnpc = PETSC_FALSE;

  snes->alwayscomputesfinalresidual = PETSC_FALSE;

  PetscCall(PetscNew(&shell));
  snes->data = (void *)shell;
  PetscCall(PetscObjectComposeFunction((PetscObject)snes, "SNESShellSetSolve_C", SNESShellSetSolve_Shell));
  PetscFunctionReturn(0);
}
