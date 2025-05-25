<?php

namespace humhub\modules\ldap\components;

use Laminas\Ldap\Ldap;
use Laminas\Ldap\Filter;
use Laminas\Ldap\Dn;
use Laminas\Ldap\Exception;
use Laminas\Ldap\ErrorHandler;

class ZendLdap extends Ldap
{
    /**
     * An LDAP search routine for finding information and returning paginated results
     * https://stackoverflow.com/questions/16892693/zf2-ldap-pagination
     *
     * Options can be either passed as single parameters according to the
     * method signature or as an array with one or more of the following keys
     * - filter
     * - baseDn
     * - scope
     * - attributes
     * - sort
     * - collectionClass
     * - sizelimit
     * - timelimit
     *
     * @param string|Filter\AbstractFilter|array $filter
     * @param string|Dn|null $basedn
     * @param int $scope
     * @param array $attributes
     * @param string|null $sort
     * @param string|null $collectionClass
     * @param int $timelimit
     * @param int $pageSize
     * @return array
     * @throws Exception\LdapException
     */
    public function multiPageSearch(
        $filter,
        $basedn,
        $scope,
        array $attributes = [],
        $sort = null,
        $collectionClass = null,
        $timelimit = 0,
        $pageSize = 10000,
    ) {
        $resolvedFilter = $filter;
        $resolvedBaseDn = $basedn;
        $resolvedAttributes = $attributes;
        $resolvedTimelimit = $timelimit;

        if (is_array($filter)) {
            $options = array_change_key_case($filter, CASE_LOWER);
            foreach ($options as $key => $value) {
                switch ($key) {
                    case 'filter':
                        $resolvedFilter = $value;
                        break;
                    case 'basedn':
                        $resolvedBaseDn = $value;
                        break;
                    case 'attributes':
                        if (is_array($value)) {
                            $resolvedAttributes = $value;
                        }
                        break;
                    case 'timelimit':
                        $resolvedTimelimit = (int)$value;
                        break;
                }
            }
        }

        if ($resolvedBaseDn === null) {
            $resolvedBaseDn = $this->getBaseDn();
        } elseif ($resolvedBaseDn instanceof Dn) {
            $resolvedBaseDn = $resolvedBaseDn->toString();
        }

        if ($resolvedFilter instanceof Filter\AbstractFilter) {
            $resolvedFilter = $resolvedFilter->toString();
        }

        $resource = $this->getResource();
        ErrorHandler::start(E_WARNING);
        $results = $this->ldapSearchPaged($resource, $resolvedBaseDn, $resolvedFilter, $resolvedAttributes, 0, $pageSize, $resolvedTimelimit);
        ErrorHandler::stop();

        if (count($results) == 0) {
            throw new Exception\LdapException($this, 'searching: ' . $resolvedFilter);
        }

        return $results;
    }

    private function ldapSearchPaged($resource, $basedn, $filter, $attributes, $attributesOnly, $sizelimit, $timelimit)
    {
        $results = [];
        $cookie = '';

        do {
            $result = ldap_search(
                $resource,
                $basedn,
                $filter,
                $attributes,
                $attributesOnly,
                0,
                $timelimit,
                null,
                [['oid' => LDAP_CONTROL_PAGEDRESULTS, 'value' => ['size' => $sizelimit, 'cookie' => $cookie]]],
            );

            $errCode = $dn = $errMsg = $refs = null;
            ldap_parse_result($resource, $result, $errCode, $dn, $errMsg, $refs, $controls);

            foreach (ldap_get_entries($resource, $result) as $item) {
                if (!is_array($item)) {
                    continue;
                }

                array_push($results, (array)$item);
            }

            $cookie = $controls[LDAP_CONTROL_PAGEDRESULTS]['value']['cookie'] ?? '';
        } while (!empty($cookie));

        return $results;
    }
}
