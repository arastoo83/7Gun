<?php
/**
 * @link https://www.humhub.org/
 * @copyright Copyright (c) HumHub GmbH & Co. KG
 * @license https://www.humhub.com/licences
 */

use humhub\modules\ui\mail\DefaultMailStyle;
use humhub\modules\ui\view\components\View;
use humhub\modules\user\models\User;
use yii\helpers\Html;

/* @var View $this */
/* @var string $approveUrl */
/* @var User $user */
/* @var string $newEmail */
?>
<tr>
    <td align="center" valign="top" class="fix-box">

        <!-- start  container width 600px -->
        <table width="600" align="center" border="0" cellspacing="0" cellpadding="0" class="container"
               style="background-color:<?= $this->theme->variable('background-color-main', '#fff') ?>">


            <tr>
                <td valign="top">

                    <!-- start container width 560px -->
                    <table width="540" align="center" border="0" cellspacing="0" cellpadding="0" class="full-width"
                           style="background-color:<?= $this->theme->variable('background-color-main', '#fff') ?>">


                        <!-- start text content -->
                        <tr>
                            <td valign="top">
                                <table width="100%" border="0" cellspacing="0" cellpadding="0" align="center">
                                    <tr>
                                        <td valign="top" width="auto" align="center">
                                            <!-- start button -->
                                            <table border="0" align="center" cellpadding="0" cellspacing="0">
                                                <tr>
                                                    <td width="auto" align="center" valign="middle" height="28"
                                                        style="background-color:<?= $this->theme->variable('background-color-main', '#fff') ?>;background-clip: padding-box; font-size:26px; font-family: <?= $this->theme->variable('mail-font-family', DefaultMailStyle::DEFAULT_FONT_FAMILY) ?>; text-align:center;  color:<?= $this->theme->variable('text-color-soft2', '#aeaeae') ?>; font-weight: 300; padding:0 18px">

                                                        <span
                                                            style="color:<?= $this->theme->variable('text-color-highlight', '#555') ?>; font-weight: 300">
                                                            <?= Yii::t('UserModule.account', '<strong>Confirm</strong></strong> your new email address') ?>
                                                        </span>
                                                    </td>
                                                </tr>
                                            </table>
                                            <!-- end button -->
                                        </td>
                                    </tr>


                                </table>
                            </td>
                        </tr>
                        <!-- end text content -->


                    </table>
                    <!-- end  container width 560px -->
                </td>
            </tr>
        </table>
        <!-- end  container width 600px -->
    </td>
</tr>

<!-- END LAYOUT-1/1 -->


<!-- START LAYOUT-1/2 -->

<tr>
    <td align="center" valign="top" class="fix-box">

        <!-- start  container width 600px -->
        <table width="600" align="center" border="0" cellspacing="0" cellpadding="0" class="container"
               style="background-color:<?= $this->theme->variable('background-color-main', '#fff') ?>; border-bottom-left-radius: 4px; border-bottom-right-radius: 4px">


            <tr>
                <td valign="top">

                    <!-- start container width 560px -->
                    <table width="540" align="center" border="0" cellspacing="0" cellpadding="0" class="full-width"
                           style="background-color:<?= $this->theme->variable('background-color-main', '#fff') ?>">


                        <!-- start text content -->
                        <tr>
                            <td valign="top">
                                <table width="100%" border="0" cellspacing="0" cellpadding="0" align="left">


                                    <!-- start text content -->
                                    <tr>
                                        <td valign="top">
                                            <table border="0" cellspacing="0" cellpadding="0" align="left">


                                                <!--start space height -->
                                                <tr>
                                                    <td height="30"></td>
                                                </tr>
                                                <!--end space height -->

                                                <tr>
                                                    <td style="font-size: 14px; line-height: 22px; font-family: <?= $this->theme->variable('mail-font-family', DefaultMailStyle::DEFAULT_FONT_FAMILY) ?>; color:<?= $this->theme->variable('text-color-main', '#777') ?>; font-weight:300; text-align:left; ">

                                                        <?= Yii::t('UserModule.account', 'Hello') ?> <?= Html::encode($user->displayName) ?>
                                                        ,<br><br>

                                                        <?= Yii::t('UserModule.account', 'You have requested to change your e-mail address.<br>Your new e-mail address is {newemail}.<br><br>To confirm your new e-mail address please click on the button below.', ['{newemail}' => Html::encode($newEmail)]) ?>

                                                    </td>
                                                </tr>

                                                <!--start space height -->
                                                <tr>
                                                    <td height="30"></td>
                                                </tr>
                                                <!--end space height -->


                                            </table>
                                        </td>
                                    </tr>
                                    <!-- end text content -->

                                    <tr>
                                        <td valign="top" width="auto" align="center">
                                            <!-- start button -->
                                            <table border="0" align="center" cellpadding="0" cellspacing="0">
                                                <tr>
                                                    <td width="auto" align="center" valign="middle" height="32"
                                                        style="background-color:<?= $this->theme->variable('primary') ?>;  border-radius:5px; background-clip: padding-box;font-size:14px; font-family: <?= $this->theme->variable('mail-font-family', DefaultMailStyle::DEFAULT_FONT_FAMILY) ?>; text-align:center;  color:<?= $this->theme->variable('text-color-contrast', '#fff') ?>; font-weight: 600; padding: 5px 30px">

                                                        <span
                                                            style="color: <?= $this->theme->variable('text-color-contrast', '#fff') ?>; font-weight: 300">
                                                            <a href="<?= $approveUrl ?>"
                                                               style="text-decoration: none; color: <?= $this->theme->variable('text-color-contrast', '#fff') ?>; font-weight: 300">
                                                                <strong><?= Yii::t('UserModule.account', 'Confirm') ?></strong>
                                                            </a>
                                                        </span>
                                                    </td>

                                                </tr>
                                            </table>
                                            <!-- end button -->
                                        </td>

                                    </tr>

                                </table>
                            </td>
                        </tr>
                        <!-- end text content -->

                        <!--start space height -->
                        <tr>
                            <td height="20"></td>
                        </tr>
                        <!--end space height -->


                    </table>
                    <!-- end  container width 560px -->
                </td>
            </tr>
        </table>
        <!-- end  container width 600px -->
    </td>
</tr>
